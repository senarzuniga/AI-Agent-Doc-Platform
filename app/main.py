"""
Streamlit web application for AI-Agent-Doc-Platform.

Run with:  streamlit run app/main.py
"""

from __future__ import annotations

import sys
import os

# Ensure project root is on the path when running from the app/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from dotenv import load_dotenv

from core.orchestrator import Orchestrator, PipelineResult

load_dotenv()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Agent-Doc-Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("AI-Agent-Doc-Platform")
    st.caption("Powered by AI-FACTORY-v2 architecture")
    st.divider()

    doc_type = st.selectbox(
        "Document type",
        options=["report", "proposal", "summary"],
        index=0,
        help="The type of document to generate.",
    )

    output_format = st.selectbox(
        "Output format",
        options=["markdown", "html", "plain"],
        index=0,
        help="Format of the final document.",
    )

    st.divider()
    st.markdown("**Pipeline stages**")
    st.markdown("1. 🔍 Research Agent")
    st.markdown("2. ✍️  Writer Agent")
    st.markdown("3. 🔎 Reviewer Agent")
    st.markdown("4. 📄 Formatter Agent")

# ── Main area ─────────────────────────────────────────────────────────────────
st.header("📄 Document Generator")
st.markdown(
    "Enter a topic and click **Generate** to run the full multi-agent pipeline."
)

topic = st.text_area(
    "Topic / prompt",
    placeholder="e.g. 'The business case for adopting renewable energy in manufacturing'",
    height=100,
)

generate_btn = st.button("🚀 Generate Document", type="primary", use_container_width=True)

if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic before generating.")
    else:
        with st.spinner("Running multi-agent pipeline…"):
            try:
                orchestrator = Orchestrator(config_path=CONFIG_PATH)
                result: PipelineResult = orchestrator.run(
                    topic.strip(),
                    doc_type=doc_type,
                    output_format=output_format,
                )
            except EnvironmentError as exc:
                st.error(f"⚠️ Configuration error: {exc}")
                st.stop()
            except Exception as exc:
                st.error(f"❌ Pipeline error: {exc}")
                st.stop()

        if result.success:
            st.success("✅ Document generated successfully!")

            tab_doc, tab_research, tab_draft = st.tabs(
                ["📄 Final Document", "🔍 Research Brief", "✍️ Initial Draft"]
            )

            with tab_doc:
                if output_format == "markdown":
                    st.markdown(result.final_document)
                elif output_format == "html":
                    st.components.v1.html(result.final_document, height=600, scrolling=True)
                else:
                    st.text(result.final_document)

                st.download_button(
                    label="⬇️ Download document",
                    data=result.final_document,
                    file_name=f"document.{output_format if output_format != 'plain' else 'txt'}",
                    mime="text/plain",
                )

            with tab_research:
                st.markdown(result.research)

            with tab_draft:
                st.markdown(result.draft)
        else:
            st.error("Pipeline completed with errors:")
            for err in result.errors:
                st.code(err)

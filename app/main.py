"""Streamlit web application for AI-Agent-Doc-Platform."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Allow imports from the project root when running via `streamlit run app/main.py`
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

import yaml  # noqa: E402 — imported after sys.path fix

from core.orchestrator import run  # noqa: E402


_PLACEHOLDER_VALUES = {
    "",
    "your_key_here",
    "your_openai_api_key_here",
    "changeme",
    "placeholder",
}


def _resolve_openai_api_key() -> str:
    """Return the effective OpenAI key, supporting common env aliases."""
    candidates = [
        os.getenv("OPENAI_API_KEY"),
        os.getenv("OPENAI_KEY"),
        os.getenv("AZURE_OPENAI_KEY"),
    ]
    for raw in candidates:
        candidate = (raw or "").strip().strip('"').strip("'")
        if candidate and candidate.lower() not in _PLACEHOLDER_VALUES:
            return candidate
    return ""


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def _load_config() -> dict:
    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH) as f:
            return yaml.safe_load(f) or {}
    return {}


config = _load_config()
app_title = config.get("app", {}).get("title", "AI-Agent-Doc-Platform")

st.set_page_config(
    page_title=app_title,
    page_icon="🤖",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input(
        "OpenAI API Key",
        value=_resolve_openai_api_key(),
        type="password",
        help="Your OpenAI API key. Can also be set via OPENAI_API_KEY or OPENAI_KEY in .env.",
    )
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key.strip()

    st.divider()
    st.markdown("### About")
    st.markdown(
        "**AI-Agent-Doc-Platform** uses a multi-agent AI pipeline "
        "(AI-FACTORY-v2 architecture) to generate professional documents:\n\n"
        "1. 🔍 **Research Agent** — gathers facts & context\n"
        "2. ✍️ **Writing Agent** — drafts the document\n"
        "3. ✅ **Review Agent** — refines & finalizes"
    )

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------

st.title(f"🤖 {app_title}")
st.caption("Multi-agent document generation powered by AI-FACTORY-v2 architecture")

st.divider()

prompt = st.text_area(
    "Document topic or request",
    placeholder=(
        "E.g. 'Generate a business report on the impact of AI in healthcare'"
    ),
    height=120,
)

col1, col2 = st.columns([1, 3])
with col1:
    save_output = st.checkbox("Save to disk", value=True)

generate_btn = st.button("🚀 Generate Document", type="primary", use_container_width=True)

if generate_btn:
    if not prompt.strip():
        st.warning("Please enter a document topic or request.")
    elif not _resolve_openai_api_key():
        st.error("OpenAI API key is required. Set it in the sidebar or .env file.")
    else:
        # Normalize alias keys so all downstream code reads OPENAI_API_KEY.
        os.environ["OPENAI_API_KEY"] = _resolve_openai_api_key()
        with st.spinner("Running multi-agent pipeline… this may take a moment ⏳"):
            try:
                result = run(prompt.strip(), save_output=save_output)
                st.success("✅ Document generated successfully!")
                st.divider()
                st.markdown("## Generated Document")
                st.markdown(result)
                st.download_button(
                    label="⬇️ Download as Markdown",
                    data=result,
                    file_name="generated_document.md",
                    mime="text/markdown",
                )
            except Exception as exc:
                st.error(f"❌ Generation failed: {exc}")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.divider()
st.caption("AI-Agent-Doc-Platform · AI-FACTORY-v2 architecture · Powered by OpenAI")

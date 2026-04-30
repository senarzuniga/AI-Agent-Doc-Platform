"""Core orchestrator for the AI-FACTORY-v2 multi-agent pipeline."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

from agents.research_agent import ResearchAgent
from agents.writing_agent import WritingAgent
from agents.review_agent import ReviewAgent

load_dotenv()

_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def _load_config() -> dict:
    """Load configuration from config.yaml."""
    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


def _agent_kwargs(config: dict, agent_key: str) -> dict:
    """Extract agent-specific kwargs from config."""
    model_cfg = config.get("model", {})
    agent_cfg = config.get("agents", {}).get(agent_key, {})
    return {
        "model": model_cfg.get("name", "gpt-4o-mini"),
        "max_tokens": agent_cfg.get("max_tokens", model_cfg.get("max_tokens", 2048)),
        "temperature": agent_cfg.get(
            "temperature", model_cfg.get("temperature", 0.7)
        ),
    }


def run(
    prompt: str,
    output_dir: Optional[str] = None,
    save_output: bool = True,
) -> str:
    """Run the full multi-agent document generation pipeline.

    Args:
        prompt: The document topic or generation request.
        output_dir: Directory to save the generated document. Defaults to
            the value in config.yaml or ``outputs/``.
        save_output: Whether to persist the result to disk.

    Returns:
        The final generated document as a Markdown string.
    """
    config = _load_config()
    max_retries = config.get("orchestrator", {}).get("max_retries", 3)
    retry_delay = config.get("orchestrator", {}).get("retry_delay", 2)

    research_agent = ResearchAgent(**_agent_kwargs(config, "research"))
    writing_agent = WritingAgent(**_agent_kwargs(config, "writing"))
    review_agent = ReviewAgent(**_agent_kwargs(config, "review"))

    for attempt in range(1, max_retries + 1):
        try:
            research_results = research_agent.run(prompt)
            draft = writing_agent.run(prompt, context=research_results)
            final_document = review_agent.run(prompt, context=draft)
            break
        except Exception as exc:
            if attempt == max_retries:
                raise RuntimeError(
                    f"Pipeline failed after {max_retries} attempts: {exc}"
                ) from exc
            time.sleep(retry_delay)

    if save_output:
        _save_document(prompt, final_document, output_dir, config)

    return final_document


def _save_document(
    prompt: str,
    document: str,
    output_dir: Optional[str],
    config: dict,
) -> Path:
    """Persist the generated document to disk and return its path."""
    raw_dir = (
        output_dir
        or config.get("app", {}).get("output_dir")
        or os.getenv("APP_OUTPUT_DIR", "outputs")
    )
    # Resolve the path and restrict it to the project root to prevent traversal
    project_root = Path(__file__).parent.parent.resolve()
    out_path = (project_root / Path(raw_dir)).resolve()
    if not str(out_path).startswith(str(project_root)):
        out_path = project_root / "outputs"
    out_path.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in prompt[:50])
    safe_name = safe_name.strip().replace(" ", "_")
    timestamp = int(time.time())
    filename = out_path / f"{safe_name}_{timestamp}.md"

    filename.write_text(document, encoding="utf-8")
    return filename

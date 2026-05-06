"""Core orchestrator for the AI-FACTORY-v2 multi-agent pipeline."""

from __future__ import annotations

import os
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from agents.research_agent import ResearchAgent
from agents.writing_agent import WritingAgent
from agents.review_agent import ReviewAgent

load_dotenv()

_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
_PROJECT_ROOT = Path(__file__).parent.parent.resolve()


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


def _output_dir(config: dict) -> Path:
    """Return the absolute output directory, always within the project root."""
    dir_name = (
        config.get("app", {}).get("output_dir")
        or os.getenv("APP_OUTPUT_DIR", "outputs")
    )
    # Only accept a simple directory name (no path separators or dot segments)
    # to prevent path traversal via config/env manipulation.
    safe_dir = Path(dir_name).name or "outputs"
    return _PROJECT_ROOT / safe_dir


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _run_agents(prompt: str, research_agent: ResearchAgent, writing_agent: WritingAgent, review_agent: ReviewAgent) -> str:
    research_results = research_agent.run(prompt)
    draft = writing_agent.run(prompt, context=research_results)
    final_document = review_agent.run(prompt, context=draft)
    return final_document


def run(
    prompt: str,
    save_output: bool = True,
) -> str:
    """Run the full multi-agent document generation pipeline.

    Args:
        prompt: The document topic or generation request.
        save_output: Whether to persist the result to disk.

    Returns:
        The final generated document as a Markdown string.
    """
    config = _load_config()

    research_agent = ResearchAgent(**_agent_kwargs(config, "research"))
    writing_agent = WritingAgent(**_agent_kwargs(config, "writing"))
    review_agent = ReviewAgent(**_agent_kwargs(config, "review"))

    final_document = _run_agents(prompt, research_agent, writing_agent, review_agent)

    if save_output:
        _save_document(prompt, final_document, config)

    return final_document


def _save_document(
    prompt: str,
    document: str,
    config: dict,
) -> Path:
    """Persist the generated document to disk and return its path."""
    out_path = _output_dir(config)
    out_path.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in prompt[:50])
    safe_name = safe_name.strip().replace(" ", "_")
    timestamp = int(time.time())
    filename = out_path / f"{safe_name}_{timestamp}.md"

    filename.write_text(document, encoding="utf-8")
    return filename

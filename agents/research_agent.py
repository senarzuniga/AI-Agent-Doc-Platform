"""
Research Agent – gathers context, key facts, and background information
for a given topic using the LLM as a knowledge base.
"""

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent

_SYSTEM_PROMPT = """You are a thorough research assistant.
Given a topic, produce a structured research brief that includes:
- An executive summary (2–3 sentences)
- Key facts and statistics (bullet points)
- Relevant background context
- Important considerations or caveats

Be factual, concise, and well-organised. Do not fabricate statistics."""


class ResearchAgent(BaseAgent):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)

    def run(self, topic: str) -> str:
        """Return a research brief for *topic*."""
        user_prompt = f"Research topic: {topic}\n\nProvide a comprehensive research brief."
        return self._chat(_SYSTEM_PROMPT, user_prompt)

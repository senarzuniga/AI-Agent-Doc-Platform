"""Research Agent — gathers facts and context for document generation."""

from __future__ import annotations

from typing import Optional

from agents.base_agent import BaseAgent

_SYSTEM_PROMPT = """You are an expert research analyst. Your task is to gather
relevant facts, statistics, key concepts, and context on a given topic.
Structure your output as numbered bullet points covering:
1. Overview and definition
2. Key facts and statistics
3. Important concepts or terminology
4. Relevant background context
Be concise, factual, and comprehensive."""


class ResearchAgent(BaseAgent):
    """Gathers research data and context for a document topic."""

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("temperature", 0.3)
        super().__init__(
            name="Research Agent",
            description="Gathers facts, data, and context for the document topic",
            **kwargs,
        )

    def run(self, prompt: str, context: Optional[str] = None) -> str:
        """Research the given topic and return structured findings."""
        user_message = f"Research the following topic thoroughly:\n\n{prompt}"
        if context:
            user_message += f"\n\nAdditional context:\n{context}"
        return self._chat(_SYSTEM_PROMPT, user_message)

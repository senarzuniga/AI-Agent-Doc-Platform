"""Writing Agent — drafts professional document content."""

from __future__ import annotations

from typing import Optional

from agents.base_agent import BaseAgent

_SYSTEM_PROMPT = """You are an expert professional document writer. Your task is
to create well-structured, clear, and comprehensive documents based on a topic
and research data provided to you.
Your documents must include:
- A clear executive summary
- Organized sections with headings
- Professional language appropriate for business or technical audiences
- Conclusions and actionable insights where relevant
Format the output in clean Markdown."""


class WritingAgent(BaseAgent):
    """Drafts structured, professional document content."""

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("temperature", 0.7)
        kwargs.setdefault("max_tokens", 4096)
        super().__init__(
            name="Writing Agent",
            description="Drafts structured, professional document content",
            **kwargs,
        )

    def run(self, prompt: str, context: Optional[str] = None) -> str:
        """Draft a professional document based on the prompt and research context."""
        user_message = f"Write a professional document about:\n\n{prompt}"
        if context:
            user_message += f"\n\nUse the following research findings:\n{context}"
        return self._chat(_SYSTEM_PROMPT, user_message)

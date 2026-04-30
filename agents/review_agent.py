"""Review Agent — reviews and refines document quality."""

from __future__ import annotations

from typing import Optional

from agents.base_agent import BaseAgent

_SYSTEM_PROMPT = """You are an expert editor and quality reviewer. Your task is
to review a draft document and improve it for:
- Clarity and readability
- Logical flow and structure
- Grammar and style
- Completeness and accuracy
- Professional tone
Return the improved, final document in clean Markdown. Do not add commentary
about the changes—only return the improved document itself."""


class ReviewAgent(BaseAgent):
    """Reviews, improves, and finalizes document quality."""

    def __init__(self, **kwargs) -> None:
        super().__init__(
            name="Review Agent",
            description="Reviews, improves, and finalizes document quality",
            temperature=0.4,
            **kwargs,
        )

    def run(self, prompt: str, context: Optional[str] = None) -> str:
        """Review and refine the draft document."""
        if context is None:
            return prompt
        user_message = (
            f"Review and improve the following document draft about '{prompt}':\n\n"
            f"{context}"
        )
        return self._chat(_SYSTEM_PROMPT, user_message)

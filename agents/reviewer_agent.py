"""
Reviewer Agent – critiques and improves a document draft.
"""

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent

_SYSTEM_PROMPT = """You are a senior editor and document quality reviewer.
Review the draft document and return an improved version that:
- Fixes any grammatical or stylistic issues
- Improves clarity and flow
- Ensures consistency in tone and formatting
- Strengthens weak arguments or unsupported claims
- Removes redundancy

Return ONLY the revised document text, without meta-commentary about what you changed."""


class ReviewerAgent(BaseAgent):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)

    def run(self, draft: str) -> str:
        """Return an improved version of *draft*."""
        user_prompt = f"Please review and improve the following document:\n\n{draft}"
        return self._chat(_SYSTEM_PROMPT, user_prompt)

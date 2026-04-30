"""
Formatter Agent – converts a reviewed document into the requested output format.
"""

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent

_SYSTEM_PROMPTS: dict[str, str] = {
    "markdown": """You are a Markdown formatting specialist.
Convert the document to clean, well-structured Markdown:
- Use # / ## / ### headings appropriately
- Use bullet lists (- ) and numbered lists where applicable
- Bold (**) key terms
- Use > for important quotes or callouts
- Ensure blank lines between sections

Return ONLY the formatted Markdown.""",

    "html": """You are an HTML formatting specialist.
Convert the document to semantic HTML5:
- Use <h1>, <h2>, <h3> for headings
- Use <p> for paragraphs
- Use <ul>/<li> and <ol>/<li> for lists
- Use <strong> for key terms
- Wrap the document in <article> tags

Return ONLY the HTML markup (no <html>/<body> wrapper).""",

    "plain": """You are a plain-text formatter.
Convert the document to clean plain text:
- Use UPPERCASE for section headings
- Use dashes (---) to separate sections
- Use * or - for bullet points
- Keep line width under 80 characters

Return ONLY the plain text.""",
}

_DEFAULT_FORMAT = "markdown"


class FormatterAgent(BaseAgent):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)

    def run(self, document: str, output_format: str = "markdown") -> str:
        """Return *document* formatted as *output_format*."""
        system_prompt = _SYSTEM_PROMPTS.get(output_format, _SYSTEM_PROMPTS[_DEFAULT_FORMAT])
        user_prompt = f"Format the following document:\n\n{document}"
        return self._chat(system_prompt, user_prompt)

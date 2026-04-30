"""
Writer Agent – composes a structured document draft from a research brief.
"""

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent

_SYSTEM_PROMPTS: dict[str, str] = {
    "report": """You are a professional business report writer.
Using the research brief provided, write a well-structured report with:
- Executive Summary
- Introduction
- Main Findings (with sub-sections as appropriate)
- Analysis
- Recommendations
- Conclusion

Use clear, professional language. Support claims with the data from the research brief.""",

    "proposal": """You are a persuasive proposal writer.
Using the research brief, write a compelling proposal with:
- Overview / Problem Statement
- Proposed Solution
- Benefits and Value Proposition
- Implementation Approach
- Budget Considerations
- Next Steps""",

    "summary": """You are a concise executive summariser.
Using the research brief, produce a clear executive summary that:
- States the key issue or topic in one sentence
- Summarises the most important findings (3–5 bullet points)
- Provides a brief recommendation or conclusion""",
}

_DEFAULT_SYSTEM_PROMPT = _SYSTEM_PROMPTS["report"]


class WriterAgent(BaseAgent):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)

    def run(self, topic: str, research: str, doc_type: str = "report") -> str:
        """Return a document draft for *topic* using the provided *research*."""
        system_prompt = _SYSTEM_PROMPTS.get(doc_type, _DEFAULT_SYSTEM_PROMPT)
        user_prompt = (
            f"Topic: {topic}\n\n"
            f"Research Brief:\n{research}\n\n"
            "Please write the document now."
        )
        return self._chat(system_prompt, user_prompt)

"""
Base class shared by all AI-FACTORY-v2 agents.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import openai

logger = logging.getLogger(__name__)


class BaseAgent:
    """Abstract base agent providing shared OpenAI client setup."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        api_key = os.getenv("OPENAI_API_KEY") or config.get("openai", {}).get("api_key", "")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY is not set. Add it to your .env file or environment variables."
            )
        self.client = openai.OpenAI(api_key=api_key)
        self.model: str = config.get("openai", {}).get("model", "gpt-4o-mini")
        self.temperature: float = float(config.get("openai", {}).get("temperature", 0.7))
        self.max_tokens: int = int(config.get("openai", {}).get("max_tokens", 2048))

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""

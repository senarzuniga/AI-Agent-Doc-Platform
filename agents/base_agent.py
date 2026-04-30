"""Base agent class for the AI-FACTORY-v2 architecture."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Optional

from openai import OpenAI


class BaseAgent(ABC):
    """Abstract base class for all AI agents in the platform."""

    def __init__(
        self,
        name: str,
        description: str,
        model: str = "gpt-4o-mini",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        api_key: Optional[str] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """Send a chat completion request and return the response text."""
        response = self._client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""

    @abstractmethod
    def run(self, prompt: str, context: Optional[str] = None) -> str:
        """Execute the agent's primary task."""

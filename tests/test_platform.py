"""Unit tests for AI-Agent-Doc-Platform."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from tenacity import RetryError

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# BaseAgent
# ---------------------------------------------------------------------------


class TestBaseAgent:
    def _make_agent(self):
        from agents.base_agent import BaseAgent

        class ConcreteAgent(BaseAgent):
            def run(self, prompt, context=None):
                return self._chat("system", prompt)

        with patch("agents.base_agent.OpenAI"):
            agent = ConcreteAgent(
                name="Test",
                description="Test agent",
                api_key="test-key",
            )
        return agent

    def test_attributes(self):
        agent = self._make_agent()
        assert agent.name == "Test"
        assert agent.description == "Test agent"

    def test_chat_returns_content(self):
        agent = self._make_agent()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "hello"
        agent._client.chat.completions.create.return_value = mock_response
        result = agent._chat("sys", "user")
        assert result == "hello"


# ---------------------------------------------------------------------------
# ResearchAgent
# ---------------------------------------------------------------------------


class TestResearchAgent:
    def _make_agent(self):
        with patch("agents.base_agent.OpenAI"):
            from agents.research_agent import ResearchAgent

            return ResearchAgent(api_key="test-key")

    def test_name(self):
        agent = self._make_agent()
        assert "Research" in agent.name

    def test_run_calls_chat(self):
        agent = self._make_agent()
        agent._chat = MagicMock(return_value="research output")
        result = agent.run("AI in healthcare")
        assert result == "research output"
        agent._chat.assert_called_once()


# ---------------------------------------------------------------------------
# WritingAgent
# ---------------------------------------------------------------------------


class TestWritingAgent:
    def _make_agent(self):
        with patch("agents.base_agent.OpenAI"):
            from agents.writing_agent import WritingAgent

            return WritingAgent(api_key="test-key")

    def test_name(self):
        agent = self._make_agent()
        assert "Writing" in agent.name

    def test_run_includes_context(self):
        agent = self._make_agent()
        captured = {}

        def fake_chat(system, user):
            captured["user"] = user
            return "draft"

        agent._chat = fake_chat
        agent.run("climate change", context="fact1\nfact2")
        assert "fact1" in captured["user"]


# ---------------------------------------------------------------------------
# ReviewAgent
# ---------------------------------------------------------------------------


class TestReviewAgent:
    def _make_agent(self):
        with patch("agents.base_agent.OpenAI"):
            from agents.review_agent import ReviewAgent

            return ReviewAgent(api_key="test-key")

    def test_name(self):
        agent = self._make_agent()
        assert "Review" in agent.name

    def test_run_without_context_returns_prompt(self):
        agent = self._make_agent()
        result = agent.run("some prompt")
        assert result == "some prompt"

    def test_run_with_context_calls_chat(self):
        agent = self._make_agent()
        agent._chat = MagicMock(return_value="final doc")
        result = agent.run("topic", context="draft text")
        assert result == "final doc"


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


class TestOrchestrator:
    def test_run_pipeline(self, monkeypatch):
        with (
            patch("agents.base_agent.OpenAI"),
            patch("core.orchestrator.ResearchAgent") as MockResearch,
            patch("core.orchestrator.WritingAgent") as MockWriting,
            patch("core.orchestrator.ReviewAgent") as MockReview,
            patch("core.orchestrator._save_document") as MockSave,
        ):
            MockResearch.return_value.run.return_value = "research"
            MockWriting.return_value.run.return_value = "draft"
            MockReview.return_value.run.return_value = "final document"

            from core.orchestrator import run

            result = run("test topic", save_output=True)

        assert result == "final document"
        MockSave.assert_called_once()

    def test_run_no_save(self):
        with (
            patch("agents.base_agent.OpenAI"),
            patch("core.orchestrator.ResearchAgent") as MockResearch,
            patch("core.orchestrator.WritingAgent") as MockWriting,
            patch("core.orchestrator.ReviewAgent") as MockReview,
        ):
            MockResearch.return_value.run.return_value = "research"
            MockWriting.return_value.run.return_value = "draft"
            MockReview.return_value.run.return_value = "final"

            from core.orchestrator import run

            result = run("test topic", save_output=False)

        assert result == "final"

    def test_retry_logic(self):
        with (
            patch("agents.base_agent.OpenAI"),
            patch("core.orchestrator.ResearchAgent") as MockResearch,
            patch("core.orchestrator.WritingAgent") as MockWriting,
            patch("core.orchestrator.ReviewAgent") as MockReview,
        ):
            MockResearch.return_value.run.side_effect = [Exception("Transient error"), "research"]
            MockWriting.return_value.run.return_value = "draft"
            MockReview.return_value.run.return_value = "final document"

            from core.orchestrator import run

            result = run("test topic", save_output=False)

        assert result == "final document"

    def test_retry_exceeds_attempts(self):
        with (
            patch("agents.base_agent.OpenAI"),
            patch("core.orchestrator.ResearchAgent") as MockResearch,
            patch("core.orchestrator.WritingAgent") as MockWriting,
            patch("core.orchestrator.ReviewAgent") as MockReview,
        ):
            MockResearch.return_value.run.side_effect = Exception("Persistent error")

            from core.orchestrator import run

            with pytest.raises(RetryError):
                run("test topic", save_output=False)

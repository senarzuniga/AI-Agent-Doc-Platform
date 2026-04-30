"""
Tests for individual agent classes.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent
from agents.formatter_agent import FormatterAgent


MINIMAL_CONFIG = {
    "openai": {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 512,
        "api_key": "test-key",
    }
}


def _make_mock_client(content: str = "mock output") -> MagicMock:
    mock_response = MagicMock()
    mock_response.choices[0].message.content = content
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture(autouse=True)
def patch_openai():
    mock_client = _make_mock_client()
    with patch("agents.base_agent.openai.OpenAI", return_value=mock_client):
        yield mock_client


class TestResearchAgent:
    def test_run_returns_string(self):
        agent = ResearchAgent(MINIMAL_CONFIG)
        result = agent.run("electric vehicles")
        assert isinstance(result, str)
        assert result == "mock output"

    def test_run_calls_chat(self):
        agent = ResearchAgent(MINIMAL_CONFIG)
        agent.run("topic")
        assert agent.client.chat.completions.create.called


class TestWriterAgent:
    def test_run_returns_string(self):
        agent = WriterAgent(MINIMAL_CONFIG)
        result = agent.run("topic", "some research", "report")
        assert isinstance(result, str)

    def test_run_with_all_doc_types(self):
        agent = WriterAgent(MINIMAL_CONFIG)
        for doc_type in ("report", "proposal", "summary"):
            result = agent.run("topic", "research", doc_type)
            assert result  # not empty

    def test_run_with_unknown_doc_type_falls_back(self):
        agent = WriterAgent(MINIMAL_CONFIG)
        result = agent.run("topic", "research", "unknown_type")
        assert isinstance(result, str)


class TestReviewerAgent:
    def test_run_returns_string(self):
        agent = ReviewerAgent(MINIMAL_CONFIG)
        result = agent.run("draft text")
        assert isinstance(result, str)


class TestFormatterAgent:
    def test_run_with_markdown(self):
        agent = FormatterAgent(MINIMAL_CONFIG)
        result = agent.run("document text", "markdown")
        assert isinstance(result, str)

    def test_run_with_html(self):
        agent = FormatterAgent(MINIMAL_CONFIG)
        result = agent.run("document text", "html")
        assert isinstance(result, str)

    def test_run_with_plain(self):
        agent = FormatterAgent(MINIMAL_CONFIG)
        result = agent.run("document text", "plain")
        assert isinstance(result, str)

    def test_run_with_unknown_format_falls_back_to_markdown(self):
        agent = FormatterAgent(MINIMAL_CONFIG)
        result = agent.run("document text", "unknown")
        assert isinstance(result, str)

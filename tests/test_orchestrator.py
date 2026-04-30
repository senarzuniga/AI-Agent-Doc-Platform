"""
Tests for the Orchestrator and individual agents.

These tests mock the OpenAI API so no real API key is needed.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from core.orchestrator import Orchestrator, PipelineResult, run


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def mock_openai(monkeypatch):
    """Patch openai.OpenAI so no real API calls are made."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "mock response"

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("agents.base_agent.openai.OpenAI", return_value=mock_client):
        yield mock_client


@pytest.fixture(scope="function")
def orchestrator(mock_openai, tmp_path):
    """Return an Orchestrator backed by a minimal config."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "openai:\n  model: gpt-4o-mini\n  temperature: 0.7\n  max_tokens: 512\n"
    )
    return Orchestrator(config_path=str(config_file))


# ── Orchestrator tests ────────────────────────────────────────────────────────

class TestOrchestrator:
    def test_run_returns_pipeline_result(self, orchestrator):
        result = orchestrator.run("test topic")
        assert isinstance(result, PipelineResult)

    def test_run_success(self, orchestrator):
        result = orchestrator.run("renewable energy")
        assert result.success
        assert result.final_document == "mock response"
        assert result.errors == []

    def test_run_populates_all_stages(self, orchestrator):
        result = orchestrator.run("AI in healthcare")
        assert result.research
        assert result.draft
        assert result.review
        assert result.final_document

    def test_run_with_different_doc_types(self, orchestrator):
        for doc_type in ("report", "proposal", "summary"):
            result = orchestrator.run("test", doc_type=doc_type)
            assert result.success, f"Failed for doc_type={doc_type}"

    def test_run_with_different_output_formats(self, orchestrator):
        for fmt in ("markdown", "html", "plain"):
            result = orchestrator.run("test", output_format=fmt)
            assert result.success, f"Failed for output_format={fmt}"

    def test_run_handles_agent_error(self, orchestrator):
        orchestrator.research_agent.run = MagicMock(side_effect=RuntimeError("API error"))
        result = orchestrator.run("failing topic")
        assert not result.success
        assert "API error" in result.errors[0]


class TestConvenienceWrapper:
    def test_run_returns_string(self, orchestrator, monkeypatch):
        monkeypatch.setattr("core.orchestrator.Orchestrator", lambda **_: orchestrator)
        document = run("test topic")
        assert isinstance(document, str)
        assert document == "mock response"

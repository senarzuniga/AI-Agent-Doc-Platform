"""
Core orchestrator for the AI-FACTORY-v2 multi-agent pipeline.

Coordinates the research → write → review → format pipeline.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import yaml

from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent
from agents.formatter_agent import FormatterAgent

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    topic: str
    research: str = ""
    draft: str = ""
    review: str = ""
    final_document: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return bool(self.final_document) and not self.errors


class Orchestrator:
    """AI-FACTORY-v2 multi-agent orchestrator.

    Pipeline:
        1. ResearchAgent  – gathers context and key facts
        2. WriterAgent    – composes the initial draft
        3. ReviewerAgent  – critiques and improves the draft
        4. FormatterAgent – applies the requested output format
    """

    def __init__(self, config_path: str = "config.yaml") -> None:
        with open(config_path, "r") as fh:
            self.config = yaml.safe_load(fh)

        self.research_agent = ResearchAgent(self.config)
        self.writer_agent = WriterAgent(self.config)
        self.reviewer_agent = ReviewerAgent(self.config)
        self.formatter_agent = FormatterAgent(self.config)

    def run(self, topic: str, doc_type: str = "report", output_format: str = "markdown") -> PipelineResult:
        """Execute the full multi-agent pipeline for *topic*."""
        result = PipelineResult(topic=topic)
        logger.info("Starting pipeline for topic: %s", topic)

        try:
            logger.info("Step 1/4 – Research")
            result.research = self.research_agent.run(topic)

            logger.info("Step 2/4 – Writing (%s)", doc_type)
            result.draft = self.writer_agent.run(topic, result.research, doc_type)

            logger.info("Step 3/4 – Review")
            result.review = self.reviewer_agent.run(result.draft)

            logger.info("Step 4/4 – Format (%s)", output_format)
            result.final_document = self.formatter_agent.run(result.review, output_format)

        except Exception as exc:
            logger.error("Pipeline error: %s", exc, exc_info=True)
            result.errors.append(str(exc))

        return result


def run(topic: str, doc_type: str = "report", output_format: str = "markdown", config_path: str = "config.yaml") -> str:
    """Convenience wrapper – returns the final document string."""
    orchestrator = Orchestrator(config_path=config_path)
    result = orchestrator.run(topic, doc_type=doc_type, output_format=output_format)
    if not result.success:
        raise RuntimeError(f"Pipeline failed: {result.errors}")
    return result.final_document

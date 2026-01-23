"""
Epistemic Indicator definitions and utilities.

Provides clear differentiation of response types to prevent false
certainty about interpretive matters.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class IndicatorType(str, Enum):
    """Types of epistemic indicators."""

    FACTUAL = "FACTUAL"
    INTERPRETIVE = "INTERPRETIVE"
    DEFERRED = "DEFERRED"

    @property
    def tag(self) -> str:
        """Get the inline tag format."""
        return f"[{self.value}]"

    @property
    def description(self) -> str:
        """Get a human-readable description."""
        descriptions = {
            IndicatorType.FACTUAL: "Verifiable information that can be checked against sources",
            IndicatorType.INTERPRETIVE: "AI-assisted analysis requiring researcher verification",
            IndicatorType.DEFERRED: "Matters requiring human judgment that AI cannot determine",
        }
        return descriptions[self]

    @property
    def examples(self) -> list[str]:
        """Get examples of content that falls under this indicator."""
        examples = {
            IndicatorType.FACTUAL: [
                "Dates, names, bibliographic data",
                "Direct quotations with citations",
                "Definition of terms (from specified source)",
                "Historical events (with scholarly consensus)",
            ],
            IndicatorType.INTERPRETIVE: [
                "Connections between texts/concepts",
                "Thematic patterns across sources",
                "Structural analysis of arguments",
                "Comparative observations",
            ],
            IndicatorType.DEFERRED: [
                "Theological truth claims",
                "Value judgments about religious practices",
                "'Correct' interpretation of contested passages",
                "Assessment of spiritual significance",
            ],
        }
        return examples[self]

    @classmethod
    def from_tag(cls, tag: str) -> "IndicatorType | None":
        """Parse an indicator type from a tag string."""
        tag = tag.strip("[]").upper()
        try:
            return cls(tag)
        except ValueError:
            return None


@dataclass
class EpistemicIndicator:
    """
    An epistemic indicator attached to a piece of content.

    Attributes:
        indicator_type: The type of indicator (FACTUAL/INTERPRETIVE/DEFERRED)
        confidence: Confidence score (0.0 to 1.0) for the classification
        content: The content this indicator applies to
        rationale: Optional explanation for why this classification was chosen
    """

    indicator_type: IndicatorType
    confidence: float
    content: str
    rationale: str | None = None

    def __post_init__(self) -> None:
        """Validate the confidence score."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")

    @property
    def tag(self) -> str:
        """Get the inline tag for this indicator."""
        return self.indicator_type.tag

    @property
    def tagged_content(self) -> str:
        """Get the content with the indicator tag prepended."""
        return f"{self.tag} {self.content}"

    @property
    def needs_review(self) -> bool:
        """Check if this indicator suggests human review is needed."""
        # DEFERRED always needs review
        if self.indicator_type == IndicatorType.DEFERRED:
            return True
        # Low confidence INTERPRETIVE needs review
        if self.indicator_type == IndicatorType.INTERPRETIVE and self.confidence < 0.5:
            return True
        return False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "indicator_type": self.indicator_type.value,
            "confidence": self.confidence,
            "content": self.content,
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EpistemicIndicator":
        """Create from dictionary."""
        return cls(
            indicator_type=IndicatorType(data["indicator_type"]),
            confidence=data["confidence"],
            content=data["content"],
            rationale=data.get("rationale"),
        )


# Keywords that suggest different indicator types
FACTUAL_MARKERS = [
    "published",
    "wrote",
    "in",  # year references like "in 1960"
    "page",
    "p.",
    "pp.",
    "according to",
    "states",
    "defined as",
    "is called",
    "born",
    "died",
    "dated",
    "located",
    "isbn",
    "doi",
]

INTERPRETIVE_MARKERS = [
    "suggests",
    "appears",
    "seems",
    "might",
    "could",
    "may",
    "possibly",
    "likely",
    "pattern",
    "connection",
    "theme",
    "similar",
    "relates",
    "resembles",
    "echoes",
    "parallels",
    "indicates",
    "implies",
    "analysis",
    "comparison",
]

DEFERRED_MARKERS = [
    "should",
    "ought",
    "must",
    "correct",
    "true",
    "false",
    "right",
    "wrong",
    "better",
    "worse",
    "sacred",
    "divine",
    "salvation",
    "sin",
    "holy",
    "righteous",
    "spiritual significance",
    "theological truth",
    "god's will",
    "meaning of life",
]

"""Tests for the epistemic indicator system."""

import pytest

from itserr_agent.core.config import AgentConfig
from itserr_agent.epistemic.classifier import EpistemicClassifier
from itserr_agent.epistemic.indicators import EpistemicIndicator, IndicatorType


class TestIndicatorType:
    """Tests for IndicatorType enum."""

    def test_tag_format(self) -> None:
        """Tags should be in [TYPE] format."""
        assert IndicatorType.FACTUAL.tag == "[FACTUAL]"
        assert IndicatorType.INTERPRETIVE.tag == "[INTERPRETIVE]"
        assert IndicatorType.DEFERRED.tag == "[DEFERRED]"

    def test_from_tag(self) -> None:
        """Should parse tags correctly."""
        assert IndicatorType.from_tag("[FACTUAL]") == IndicatorType.FACTUAL
        assert IndicatorType.from_tag("INTERPRETIVE") == IndicatorType.INTERPRETIVE
        assert IndicatorType.from_tag("[invalid]") is None

    def test_descriptions_exist(self) -> None:
        """Each indicator type should have a description."""
        for indicator in IndicatorType:
            assert indicator.description
            assert len(indicator.description) > 10


class TestEpistemicIndicator:
    """Tests for EpistemicIndicator dataclass."""

    def test_confidence_validation(self) -> None:
        """Confidence must be between 0 and 1."""
        with pytest.raises(ValueError):
            EpistemicIndicator(
                indicator_type=IndicatorType.FACTUAL,
                confidence=1.5,
                content="test",
            )

    def test_tagged_content(self) -> None:
        """Tagged content should prepend the indicator."""
        indicator = EpistemicIndicator(
            indicator_type=IndicatorType.FACTUAL,
            confidence=0.9,
            content="Gadamer published Truth and Method in 1960.",
        )
        assert indicator.tagged_content.startswith("[FACTUAL]")

    def test_needs_review_deferred(self) -> None:
        """DEFERRED always needs review."""
        indicator = EpistemicIndicator(
            indicator_type=IndicatorType.DEFERRED,
            confidence=0.95,
            content="This is the correct interpretation.",
        )
        assert indicator.needs_review is True

    def test_needs_review_low_confidence(self) -> None:
        """Low confidence INTERPRETIVE needs review."""
        indicator = EpistemicIndicator(
            indicator_type=IndicatorType.INTERPRETIVE,
            confidence=0.3,
            content="This might suggest a pattern.",
        )
        assert indicator.needs_review is True


class TestEpistemicClassifier:
    """Tests for the EpistemicClassifier."""

    @pytest.fixture
    def classifier(self) -> EpistemicClassifier:
        """Create a classifier with default config."""
        return EpistemicClassifier(AgentConfig())

    def test_citation_classified_as_factual(self, classifier: EpistemicClassifier) -> None:
        """Sentences with citations should be FACTUAL."""
        sentence = "According to Gadamer (1960), understanding is always historical."
        indicator = classifier.classify_sentence(sentence)
        assert indicator.indicator_type == IndicatorType.FACTUAL

    def test_interpretive_markers(self, classifier: EpistemicClassifier) -> None:
        """Sentences with interpretive language should be INTERPRETIVE."""
        sentence = "This pattern suggests a connection between the two texts."
        indicator = classifier.classify_sentence(sentence)
        assert indicator.indicator_type == IndicatorType.INTERPRETIVE

    def test_theological_content_deferred(self, classifier: EpistemicClassifier) -> None:
        """Theological truth claims should be DEFERRED."""
        sentence = "This is the correct interpretation of God's will."
        indicator = classifier.classify_sentence(sentence)
        assert indicator.indicator_type == IndicatorType.DEFERRED

    def test_already_tagged_preserved(self, classifier: EpistemicClassifier) -> None:
        """Already tagged content should be preserved."""
        content = "[FACTUAL] This is already tagged."
        result = classifier.classify_and_tag(content)
        assert result == content

    def test_gnorm_high_confidence(self, classifier: EpistemicClassifier) -> None:
        """High confidence GNORM annotations should be FACTUAL."""
        indicator = classifier.classify_gnorm_annotation(
            {"type": "person"},
            confidence_score=0.92,
        )
        assert indicator == IndicatorType.FACTUAL

    def test_gnorm_low_confidence(self, classifier: EpistemicClassifier) -> None:
        """Low confidence GNORM annotations should be INTERPRETIVE."""
        indicator = classifier.classify_gnorm_annotation(
            {"type": "concept"},
            confidence_score=0.45,
        )
        assert indicator == IndicatorType.INTERPRETIVE

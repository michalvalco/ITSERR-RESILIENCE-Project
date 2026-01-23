"""
Epistemic Classifier - Classifies and tags responses with epistemic indicators.

This module implements the classification pipeline that determines whether
content should be marked as FACTUAL, INTERPRETIVE, or DEFERRED.
"""

import re
from typing import Any

import structlog

from itserr_agent.core.config import AgentConfig
from itserr_agent.epistemic.indicators import (
    DEFERRED_MARKERS,
    FACTUAL_MARKERS,
    INTERPRETIVE_MARKERS,
    EpistemicIndicator,
    IndicatorType,
)

logger = structlog.get_logger()


class EpistemicClassifier:
    """
    Classifies content with epistemic indicators.

    The classifier uses a combination of:
    1. Heuristic rules (keyword detection)
    2. Pattern matching (citations, dates)
    3. Fallback to configurable default

    Design Note:
    This is a rule-based classifier for the prototype. A production
    system might use an LLM-based classifier for more nuanced decisions.
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the classifier."""
        self.config = config

        # Compile regex patterns for efficiency
        self._citation_pattern = re.compile(
            r"\([^)]*\d{4}[^)]*\)|"  # (Author 2020) style
            r"\[[^\]]*\d+[^\]]*\]|"  # [1] or [Author 2020] style
            r"p{1,2}\.\s*\d+|"  # p. 123 or pp. 123-456
            r"\d{4}[a-z]?"  # Year references
        )
        self._date_pattern = re.compile(r"\b\d{4}\b|\b\d{1,2}(st|nd|rd|th)\s+century\b")
        self._theological_pattern = re.compile(
            r"\b(god|christ|holy spirit|trinity|salvation|sin|grace|redemption|divine|sacred)\b",
            re.IGNORECASE,
        )

    def classify_and_tag(self, content: str) -> str:
        """
        Classify content and insert epistemic indicator tags.

        This processes the content sentence by sentence, classifying each
        and inserting appropriate tags.

        Args:
            content: The raw content to classify

        Returns:
            Content with epistemic indicator tags inserted
        """
        # If content already has tags, preserve them
        if re.search(r"\[(FACTUAL|INTERPRETIVE|DEFERRED)\]", content):
            logger.debug("content_already_tagged")
            return content

        # Split into sentences for classification
        sentences = self._split_sentences(content)
        classified = []

        for sentence in sentences:
            if not sentence.strip():
                classified.append(sentence)
                continue

            indicator = self.classify_sentence(sentence)
            classified.append(f"{indicator.tag} {sentence.strip()}")

        return " ".join(classified)

    def classify_sentence(self, sentence: str) -> EpistemicIndicator:
        """
        Classify a single sentence.

        Classification pipeline:
        1. Check for citation/source attribution → FACTUAL
        2. Check for theological/normative content → DEFERRED
        3. Check for interpretive markers → INTERPRETIVE
        4. Check for factual markers → FACTUAL
        5. Fallback to configured default

        Args:
            sentence: A single sentence to classify

        Returns:
            EpistemicIndicator for the sentence
        """
        sentence_lower = sentence.lower()

        # Step 1: Citation check → FACTUAL
        if self._citation_pattern.search(sentence):
            return EpistemicIndicator(
                indicator_type=IndicatorType.FACTUAL,
                confidence=0.9,
                content=sentence,
                rationale="Contains citation or source reference",
            )

        # Step 2: Theological/normative check → DEFERRED
        deferred_score = self._score_markers(sentence_lower, DEFERRED_MARKERS)
        if deferred_score >= 2 or self._contains_normative_claim(sentence_lower):
            return EpistemicIndicator(
                indicator_type=IndicatorType.DEFERRED,
                confidence=0.85,
                content=sentence,
                rationale="Contains theological or normative content",
            )

        # Step 3: Interpretive markers check
        interpretive_score = self._score_markers(sentence_lower, INTERPRETIVE_MARKERS)
        if interpretive_score >= 2:
            return EpistemicIndicator(
                indicator_type=IndicatorType.INTERPRETIVE,
                confidence=0.8,
                content=sentence,
                rationale="Contains interpretive language",
            )

        # Step 4: Factual markers check
        factual_score = self._score_markers(sentence_lower, FACTUAL_MARKERS)
        if factual_score >= 2 or self._date_pattern.search(sentence):
            return EpistemicIndicator(
                indicator_type=IndicatorType.FACTUAL,
                confidence=0.75,
                content=sentence,
                rationale="Contains factual markers or dates",
            )

        # Step 5: Fallback to default
        default_type = IndicatorType(self.config.epistemic_default)
        return EpistemicIndicator(
            indicator_type=default_type,
            confidence=0.5,
            content=sentence,
            rationale="Default classification (no strong markers)",
        )

    def _score_markers(self, text: str, markers: list[str]) -> int:
        """Count how many markers appear in the text."""
        return sum(1 for marker in markers if marker in text)

    def _contains_normative_claim(self, text: str) -> bool:
        """Check if text contains a normative or theological truth claim."""
        normative_patterns = [
            r"\bis\s+(true|false|correct|wrong)\b",
            r"\bshould\b.*\b(believe|accept|reject)\b",
            r"\bthe\s+correct\s+(interpretation|reading|understanding)\b",
            r"\bgod\s+(is|wants|desires|commands)\b",
            r"\bspiritual(ly)?\s+(true|significant|meaningful)\b",
        ]

        for pattern in normative_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _split_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences, preserving structure.

        Note: This uses a simple regex-based approach that may incorrectly split on:
        - Abbreviations (e.g., "Dr.", "St.", "etc.", "cf.")
        - Scripture references (e.g., "Gen. 1:1", "Mt. 5:3")
        - Page references (e.g., "pp. 23-45")
        - Decimal numbers

        For production use with academic/theological texts, consider using:
        - NLTK's sent_tokenize with custom abbreviations
        - spaCy's sentence segmentation
        - A custom tokenizer trained on religious studies texts

        TODO: Upgrade to more robust sentence tokenization before fellowship ends.
        """
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return sentences

    def classify_gnorm_annotation(
        self,
        annotation: dict[str, Any],
        confidence_score: float,
    ) -> IndicatorType:
        """
        Classify a GNORM annotation based on its confidence score.

        Maps GNORM confidence to epistemic indicators:
        - High confidence → FACTUAL
        - Medium confidence → INTERPRETIVE
        - Low confidence → INTERPRETIVE with review flag

        Args:
            annotation: The GNORM annotation data
            confidence_score: The confidence score (0.0 to 1.0)

        Returns:
            Appropriate IndicatorType for this annotation
        """
        if confidence_score >= self.config.high_confidence_threshold:
            return IndicatorType.FACTUAL
        elif confidence_score >= self.config.low_confidence_threshold:
            return IndicatorType.INTERPRETIVE
        else:
            # Low confidence - still INTERPRETIVE but would flag for review
            logger.debug(
                "low_confidence_annotation",
                confidence=confidence_score,
                annotation_type=annotation.get("type"),
            )
            return IndicatorType.INTERPRETIVE

    def get_classification_explanation(self, indicator: EpistemicIndicator) -> str:
        """
        Generate a human-readable explanation of the classification.

        Useful for transparency and debugging.
        """
        explanation = f"Classified as {indicator.indicator_type.value}:\n"
        explanation += f"  Confidence: {indicator.confidence:.0%}\n"
        explanation += f"  Rationale: {indicator.rationale or 'No specific rationale'}\n"
        explanation += f"  Description: {indicator.indicator_type.description}\n"

        if indicator.needs_review:
            explanation += "  ⚠️  Flagged for human review\n"

        return explanation

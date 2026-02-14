"""Tests for build_corpus_json.py — CRF consensus, disagreement, and epistemic logic."""

import sys
from pathlib import Path

# Ensure the scripts directory is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "stockel_annotation" / "scripts"))

from build_corpus_json import detect_references


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_ref(refs, text_substring):
    """Return the first ref whose text contains *text_substring*."""
    for r in refs:
        if text_substring.lower() in r["text"].lower():
            return r
    return None


# ---------------------------------------------------------------------------
# Rule-based only (baseline)
# ---------------------------------------------------------------------------

class TestRuleBasedDetection:
    """Rule-based detection without CRF input — baseline behaviour."""

    def test_biblical_with_number_is_factual(self):
        text = "See Rom. 5,12 for explanation."
        refs = detect_references(text)
        ref = _find_ref(refs, "Rom")
        assert ref is not None
        assert ref["type"] == "biblical"
        assert ref["epistemic"] == "FACTUAL"
        assert ref["confidence"] == 0.85
        assert ref["methods"] == ["rule-based"]
        assert ref["consensus"] is False

    def test_patristic_is_interpretive(self):
        text = "As Augustinus writes in his commentary."
        refs = detect_references(text)
        ref = _find_ref(refs, "Augustinus")
        assert ref is not None
        assert ref["type"] == "patristic"
        assert ref["epistemic"] == "INTERPRETIVE"
        assert ref["confidence"] == 0.75
        assert ref["methods"] == ["rule-based"]
        assert ref["consensus"] is False

    def test_confessional_is_factual(self):
        text = "In Symbolo Niceno the creed states."
        refs = detect_references(text)
        ref = _find_ref(refs, "Symbolo Niceno")
        assert ref is not None
        assert ref["type"] == "confessional"
        assert ref["epistemic"] == "FACTUAL"
        assert ref["confidence"] == 0.80

    def test_method_field_uses_plus_separator(self):
        """The 'method' string field uses ' + ' to join method names."""
        text = "See Rom. 5,12 for explanation."
        refs = detect_references(text)
        ref = _find_ref(refs, "Rom")
        assert ref["method"] == "rule-based"


# ---------------------------------------------------------------------------
# CRF consensus — both methods agree on type
# ---------------------------------------------------------------------------

class TestCRFConsensus:
    """CRF entity overlaps with rule-based match and agrees on type."""

    def test_consensus_is_factual(self):
        text = "See Augustinus in the letter."
        crf = [{"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.82}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert ref is not None
        assert ref["consensus"] is True
        assert ref["epistemic"] == "FACTUAL"
        assert "CRF" in ref["methods"]
        assert "rule-based" in ref["methods"]

    def test_consensus_boosts_confidence(self):
        text = "See Augustinus in the letter."
        crf = [{"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.82}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        # confidence = max(0.75, 0.82) + 0.05 = 0.87, capped at 0.99
        assert ref["confidence"] == 0.87

    def test_consensus_method_field(self):
        text = "See Augustinus in the letter."
        crf = [{"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.82}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert ref["method"] == "rule-based + CRF"

    def test_consensus_confidence_cap(self):
        """Confidence is capped at 0.99 even with very high CRF score."""
        text = "See Rom. 5,12 now."
        crf = [{"start": 4, "end": 12, "text": "Rom. 5,12", "type": "biblical", "confidence": 0.98}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Rom")
        assert ref["confidence"] <= 0.99


# ---------------------------------------------------------------------------
# CRF disagreement — methods disagree on type
# ---------------------------------------------------------------------------

class TestCRFDisagreement:
    """CRF entity overlaps with rule-based match but disagrees on type."""

    def test_disagreement_is_deferred(self):
        text = "See Augustinus in the letter."
        # CRF thinks it's biblical, rule-based says patristic
        crf = [{"start": 4, "end": 15, "text": "Augustinus", "type": "biblical", "confidence": 0.80}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert ref is not None
        assert ref["consensus"] is False
        assert ref["epistemic"] == "DEFERRED"
        assert ref["confidence"] == 0.65

    def test_disagreement_includes_crf_in_methods(self):
        text = "See Augustinus in the letter."
        crf = [{"start": 4, "end": 15, "text": "Augustinus", "type": "biblical", "confidence": 0.80}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert "CRF" in ref["methods"]
        assert "rule-based" in ref["methods"]


# ---------------------------------------------------------------------------
# CRF overlap — prefer matching type over first overlap (#6)
# ---------------------------------------------------------------------------

class TestCRFOverlapPreference:
    """When multiple CRF entities overlap a rule-based match,
    prefer the one whose type matches (fix for break-on-first-overlap)."""

    def test_prefers_matching_type_over_first_overlap(self):
        text = "See Augustinus in the letter."
        # Two CRF entities overlap — first disagrees, second agrees
        crf = [
            {"start": 4, "end": 15, "text": "Augustinus", "type": "biblical", "confidence": 0.70},
            {"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.85},
        ]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert ref is not None
        assert ref["consensus"] is True
        assert ref["epistemic"] == "FACTUAL"
        # Should use the matching entity's confidence
        assert ref["confidence"] == 0.90  # max(0.75, 0.85) + 0.05

    def test_selects_highest_confidence_matching_entity(self):
        """When multiple CRF entities match on type, pick the highest confidence."""
        text = "See Augustinus in the letter."
        crf = [
            {"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.70},
            {"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.92},
            {"start": 4, "end": 15, "text": "Augustinus", "type": "patristic", "confidence": 0.80},
        ]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert ref["consensus"] is True
        # Should use best confidence: max(0.75, 0.92) + 0.05 = 0.97
        assert ref["confidence"] == 0.97

    def test_disagreement_when_no_type_matches(self):
        text = "See Augustinus in the letter."
        # All overlapping CRF entities disagree on type
        crf = [
            {"start": 4, "end": 15, "text": "Augustinus", "type": "biblical", "confidence": 0.70},
            {"start": 4, "end": 15, "text": "Augustinus", "type": "reformation", "confidence": 0.80},
        ]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "Augustinus")
        assert ref["consensus"] is False
        assert ref["epistemic"] == "DEFERRED"
        assert ref["confidence"] == 0.65


# ---------------------------------------------------------------------------
# CRF-only detection (no rule-based match)
# ---------------------------------------------------------------------------

class TestCRFOnlyDetection:
    """CRF detects an entity that rules miss entirely."""

    def test_crf_only_high_confidence_is_factual(self):
        text = "Some text without recognisable patterns."
        crf = [{"start": 5, "end": 9, "text": "text", "type": "biblical", "confidence": 0.90}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "text")
        assert ref is not None
        assert ref["methods"] == ["CRF"]
        assert ref["epistemic"] == "FACTUAL"
        assert ref["consensus"] is False

    def test_crf_only_medium_confidence_is_interpretive(self):
        text = "Some text without recognisable patterns."
        crf = [{"start": 5, "end": 9, "text": "text", "type": "biblical", "confidence": 0.75}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "text")
        assert ref["epistemic"] == "INTERPRETIVE"

    def test_crf_only_low_confidence_is_deferred(self):
        """Fix #9: CRF-only with confidence <0.70 should be DEFERRED."""
        text = "Some text without recognisable patterns."
        crf = [{"start": 5, "end": 9, "text": "text", "type": "biblical", "confidence": 0.55}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "text")
        assert ref["epistemic"] == "DEFERRED"

    def test_crf_only_boundary_070_is_interpretive(self):
        """Confidence exactly 0.70 should be INTERPRETIVE, not DEFERRED."""
        text = "Some text without recognisable patterns."
        crf = [{"start": 5, "end": 9, "text": "text", "type": "biblical", "confidence": 0.70}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "text")
        assert ref["epistemic"] == "INTERPRETIVE"

    def test_crf_only_boundary_085_is_factual(self):
        """Confidence exactly 0.85 should be FACTUAL."""
        text = "Some text without recognisable patterns."
        crf = [{"start": 5, "end": 9, "text": "text", "type": "biblical", "confidence": 0.85}]
        refs = detect_references(text, crf_entities=crf)
        ref = _find_ref(refs, "text")
        assert ref["epistemic"] == "FACTUAL"

    def test_crf_only_not_covered_by_rules(self):
        """CRF-only entities should not duplicate rule-based matches."""
        text = "See Rom. 5,12 for explanation."
        # CRF covers same span as rule-based — should NOT appear as CRF-only
        crf = [{"start": 4, "end": 13, "text": "Rom. 5,12", "type": "biblical", "confidence": 0.90}]
        refs = detect_references(text, crf_entities=crf)
        # Should be exactly one reference, not two
        rom_refs = [r for r in refs if "Rom" in r["text"]]
        assert len(rom_refs) == 1
        assert "rule-based" in rom_refs[0]["methods"]


# ---------------------------------------------------------------------------
# No CRF entities provided
# ---------------------------------------------------------------------------

class TestNoCRFEntities:
    """When crf_entities is None or empty, behaviour should be unchanged."""

    def test_none_crf_entities(self):
        text = "See Rom. 5,12 for explanation."
        refs = detect_references(text, crf_entities=None)
        ref = _find_ref(refs, "Rom")
        assert ref["methods"] == ["rule-based"]
        assert ref["consensus"] is False

    def test_empty_crf_entities(self):
        text = "See Rom. 5,12 for explanation."
        refs = detect_references(text, crf_entities=[])
        ref = _find_ref(refs, "Rom")
        assert ref["methods"] == ["rule-based"]
        assert ref["consensus"] is False

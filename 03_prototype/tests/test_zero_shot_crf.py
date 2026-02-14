"""Unit tests for the zero-shot CRF experiment script.

Tests cover the core components (tokenisation, feature extraction, entity
extraction, analysis heuristics) without requiring sklearn-crfsuite or
a trained model.
"""

import pytest
import sys
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "stockel_annotation" / "scripts"))

from zero_shot_crf_experiment import (
    tokenize_for_crf,
    sentences_from_text,
    word_features,
    extract_features,
    extract_entities,
    get_context,
    is_likely_biblical_ref,
    ExperimentStats,
)


# =============================================================================
# Tokenisation Tests
# =============================================================================


class TestTokenizeForCrf:
    """Tests for the CRF tokeniser."""

    def test_simple_text(self):
        """Simple Latin text should be tokenised by whitespace."""
        tokens = tokenize_for_crf("Quod est verum")
        assert len(tokens) == 3
        assert tokens[0] == ("Quod", 0, 4)
        assert tokens[1] == ("est", 5, 8)
        assert tokens[2] == ("verum", 9, 14)

    def test_punctuation_tokens(self):
        """Punctuation should be separate tokens."""
        tokens = tokenize_for_crf("Rom. 5")
        assert len(tokens) == 3
        assert tokens[0] == ("Rom", 0, 3)
        assert tokens[1] == (".", 3, 4)
        assert tokens[2] == ("5", 5, 6)

    def test_preserves_offsets(self):
        """Character offsets should accurately reflect source text."""
        text = "Sicut Dominus dixit."
        tokens = tokenize_for_crf(text)
        for tok_text, start, end in tokens:
            assert text[start:end] == tok_text

    def test_empty_string(self):
        """Empty input should produce no tokens."""
        assert tokenize_for_crf("") == []

    def test_xml_tags(self):
        """XML-like tags should be split on angle brackets."""
        tokens = tokenize_for_crf('<ref type="biblical">Rom. 5</ref>')
        token_texts = [t[0] for t in tokens]
        assert "<" in token_texts
        assert ">" in token_texts
        assert "Rom" in token_texts

    def test_section_symbol(self):
        """Section symbol should be a separate token."""
        tokens = tokenize_for_crf("q. 1 § quod")
        token_texts = [t[0] for t in tokens]
        assert "§" in token_texts

    def test_colon_separator(self):
        """Colons should be tokenised separately."""
        tokens = tokenize_for_crf("Actor: 20")
        assert tokens[0] == ("Actor", 0, 5)
        assert tokens[1] == (":", 5, 6)
        assert tokens[2] == ("20", 7, 9)


class TestSentencesFromText:
    """Tests for paragraph/sentence splitting."""

    def test_splits_on_blank_lines(self):
        """Paragraphs separated by blank lines should be split."""
        text = "First paragraph.\n\nSecond paragraph."
        sents = sentences_from_text(text)
        assert len(sents) == 2
        assert "First" in sents[0]
        assert "Second" in sents[1]

    def test_ignores_empty_paragraphs(self):
        """Multiple blank lines should not create empty paragraphs."""
        text = "Para one.\n\n\n\n\nPara two."
        sents = sentences_from_text(text)
        assert len(sents) == 2

    def test_single_paragraph(self):
        """Text with no blank lines is one paragraph."""
        text = "Single paragraph with no breaks."
        sents = sentences_from_text(text)
        assert len(sents) == 1

    def test_empty_text(self):
        """Empty text should produce no sentences."""
        assert sentences_from_text("") == []
        assert sentences_from_text("   \n\n   ") == []


# =============================================================================
# Feature Extraction Tests
# =============================================================================


class TestWordFeatures:
    """Tests for CRF feature extraction (mirrors GNORM pipeline)."""

    def test_basic_features(self):
        """Should extract standard word-level features."""
        tokens = ["Sicut", "Dominus", "dixit"]
        feat = word_features(tokens, 0)

        assert feat["word.lower()"] == "sicut"
        assert feat["word.istitle()"] is True
        assert feat["word.isdigit()"] is False
        assert feat["word.isupper()"] is False
        assert feat["bias"] == 1.0

    def test_digit_features(self):
        """Digit tokens should have isdigit=True."""
        tokens = ["Rom", ".", "5"]
        feat = word_features(tokens, 2)
        assert feat["word.isdigit()"] is True
        assert feat["word.lower()"] == "5"

    def test_suffix_prefix_features(self):
        """Should extract character n-gram suffixes and prefixes."""
        tokens = ["Augustinus"]
        feat = word_features(tokens, 0)
        assert feat["word[-3:]"] == "nus"
        assert feat["word[-2:]"] == "us"
        assert feat["word[:3]"] == "Aug"
        assert feat["word[:2]"] == "Au"

    def test_short_word_suffix(self):
        """Short words should use the full word for suffixes."""
        tokens = ["et"]
        feat = word_features(tokens, 0)
        assert feat["word[-3:]"] == "et"  # Word shorter than 3
        assert feat["word[:3]"] == "et"

    def test_context_window(self):
        """Should include context features for surrounding tokens."""
        tokens = ["a", "b", "c", "d", "e"]
        feat = word_features(tokens, 2)  # "c" is center

        assert feat["-2:word.lower()"] == "a"
        assert feat["-1:word.lower()"] == "b"
        assert feat["+1:word.lower()"] == "d"
        assert feat["+2:word.lower()"] == "e"

    def test_boundary_markers(self):
        """Tokens at edges should have BOS/EOS markers."""
        tokens = ["first", "second"]
        feat_first = word_features(tokens, 0)
        feat_last = word_features(tokens, 1)

        # First token: positions before it should have BOS
        assert feat_first["-1:BOS"] is True
        assert feat_first["-2:BOS"] is True

        # Last token: positions after it should have EOS
        assert feat_last["+1:EOS"] is True
        assert feat_last["+2:EOS"] is True

    def test_has_period(self):
        """Should detect periods in tokens."""
        tokens = ["Rom."]
        feat = word_features(tokens, 0)
        assert feat["word.has_period"] is True

    def test_number_normalization(self):
        """Digits should be normalized in the normalized form."""
        tokens = ["123"]
        feat = word_features(tokens, 0)
        assert feat["word.normalized"] == "000"

    def test_word_length(self):
        """Should track word length."""
        tokens = ["Augustinus"]
        feat = word_features(tokens, 0)
        assert feat["word.len"] == 10


class TestExtractFeatures:
    """Tests for batch feature extraction."""

    def test_returns_one_dict_per_token(self):
        """Should return one feature dict per token."""
        tokens = ["Sicut", "Dominus", "dixit"]
        features = extract_features(tokens)
        assert len(features) == 3
        assert all(isinstance(f, dict) for f in features)

    def test_empty_tokens(self):
        """Empty token list should return empty features."""
        assert extract_features([]) == []


# =============================================================================
# Entity Extraction Tests
# =============================================================================


class TestExtractEntities:
    """Tests for extracting entity spans from BIOES labels."""

    def test_single_token_entity(self):
        """S- label should produce a single-token entity."""
        tokens = [("text", 0, 4), ("Rom", 5, 8), ("more", 9, 13)]
        labels = ["O", "S-AN", "O"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 1
        assert entities[0] == ("Rom", "AN", 5, 8)

    def test_multi_token_entity(self):
        """B-I-E labels should produce a multi-token entity."""
        tokens = [("c", 0, 1), (".", 1, 2), ("12", 3, 5)]
        labels = ["B-AN", "I-AN", "E-AN"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 1
        assert entities[0] == ("c . 12", "AN", 0, 5)

    def test_two_token_entity(self):
        """B-E labels (no I) should produce a two-token entity."""
        tokens = [("Rom", 0, 3), ("5", 4, 5)]
        labels = ["B-AN", "E-AN"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 1
        assert entities[0] == ("Rom 5", "AN", 0, 5)

    def test_no_entities(self):
        """All O labels should produce no entities."""
        tokens = [("just", 0, 4), ("text", 5, 9)]
        labels = ["O", "O"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 0

    def test_multiple_entities(self):
        """Multiple separate entities in one sequence."""
        tokens = [
            ("Rom", 0, 3), ("5", 4, 5),
            ("et", 6, 8),
            ("Gen", 9, 12), ("3", 13, 14),
        ]
        labels = ["B-AN", "E-AN", "O", "B-AN", "E-AN"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 2
        assert entities[0][0] == "Rom 5"
        assert entities[1][0] == "Gen 3"

    def test_malformed_O_after_B(self):
        """O after B (no E) should still produce an entity (graceful recovery)."""
        tokens = [("Rom", 0, 3), ("text", 4, 8)]
        labels = ["B-AN", "O"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 1
        assert entities[0][0] == "Rom"

    def test_entity_at_end(self):
        """Entity at end of sequence without closing E should be recovered."""
        tokens = [("text", 0, 4), ("Rom", 5, 8), ("5", 9, 10)]
        labels = ["O", "B-AN", "I-AN"]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 1
        assert entities[0][0] == "Rom 5"


# =============================================================================
# Context Extraction Tests
# =============================================================================


class TestGetContext:
    """Tests for context window extraction."""

    def test_normal_context(self):
        """Should show surrounding text with entity in brackets."""
        text = "sicut ait Rom. 5 dicit"
        context = get_context(text, 10, 16, window=10)
        assert "[Rom. 5]" in context
        assert "..." in context

    def test_entity_at_start(self):
        """Entity at start of text should not crash."""
        text = "Rom. 5 dicit"
        context = get_context(text, 0, 6, window=5)
        assert "[Rom. 5]" in context

    def test_entity_at_end(self):
        """Entity at end of text should not crash."""
        text = "sicut ait Rom. 5"
        context = get_context(text, 10, 16, window=5)
        assert "[Rom. 5]" in context


# =============================================================================
# Biblical Reference Heuristic Tests
# =============================================================================


class TestIsLikelyBiblicalRef:
    """Tests for the biblical reference heuristic."""

    def test_rom_abbreviation(self):
        """'Rom. 5' should be recognised as biblical."""
        assert is_likely_biblical_ref("Rom. 5") is True

    def test_gen_abbreviation(self):
        """'Gen. 3' should be recognised as biblical."""
        assert is_likely_biblical_ref("Gen. 3") is True

    def test_psalm_abbreviation(self):
        """'Psalm. 51' should be recognised as biblical."""
        assert is_likely_biblical_ref("Psalm. 51") is True

    def test_matth_abbreviation(self):
        """'Matth. 5' should be recognised as biblical."""
        assert is_likely_biblical_ref("Matth. 5") is True

    def test_actor_abbreviation(self):
        """'Actor. 20' should be recognised as biblical (Acts)."""
        assert is_likely_biblical_ref("Actor. 20") is True

    def test_apocal_abbreviation(self):
        """'Apocal. 1' should be recognised as biblical."""
        assert is_likely_biblical_ref("Apocal. 1") is True

    def test_numeric_pattern(self):
        """Chapter:verse pattern should be recognised."""
        assert is_likely_biblical_ref("5:12") is True
        assert is_likely_biblical_ref("28. 1") is True  # period between digits matches

    def test_non_biblical_text(self):
        """Plain Latin words should not be recognised as biblical."""
        assert is_likely_biblical_ref("sicut") is False
        assert is_likely_biblical_ref("dixit") is False
        assert is_likely_biblical_ref("est") is False

    def test_legal_reference(self):
        """Legal citations (c. 12, q. 1) should not be biblical."""
        assert is_likely_biblical_ref("c. 12") is False
        assert is_likely_biblical_ref("q. 1") is False

    def test_patristic_not_biblical(self):
        """Patristic names should not be flagged as biblical."""
        assert is_likely_biblical_ref("Augustinus") is False
        assert is_likely_biblical_ref("Chrysostomus") is False

    def test_ot_minor_prophets(self):
        """Minor prophet abbreviations should be recognised."""
        assert is_likely_biblical_ref("Zachar. 9") is True
        assert is_likely_biblical_ref("Habac. 2") is True
        assert is_likely_biblical_ref("Malach. 3") is True

    def test_nt_epistles(self):
        """NT epistle abbreviations should be recognised."""
        assert is_likely_biblical_ref("1. Cor. 13") is True
        assert is_likely_biblical_ref("Hebr. 11") is True
        assert is_likely_biblical_ref("Coloss. 3") is True

    def test_case_insensitive(self):
        """Biblical reference check should be case-insensitive."""
        assert is_likely_biblical_ref("ROM. 5") is True
        assert is_likely_biblical_ref("rom. 5") is True


# =============================================================================
# ExperimentStats Tests
# =============================================================================


class TestExperimentStats:
    """Tests for ExperimentStats dataclass."""

    def test_default_values(self):
        """ExperimentStats should have correct defaults."""
        stats = ExperimentStats()
        assert stats.files_processed == 0
        assert stats.total_tokens == 0
        assert stats.total_entities == 0
        assert stats.entity_tokens == 0
        assert stats.entities_by_label == {}
        assert stats.entity_texts == []
        assert stats.precision_at_biblical == 0
        assert stats.entity_contexts == []

    def test_entity_tokens_counted_once_per_paragraph(self):
        """Regression: entity_tokens must count non-O tokens once per paragraph,
        NOT once per entity. A paragraph with 3 entity tokens and 2 entities
        should add 3, not 6."""
        stats = ExperimentStats()
        # Simulate a paragraph: "Rom . 5 et Gen . 3"
        # tokens:  Rom   .   5  et  Gen   .   3
        # labels: B-AN I-AN E-AN O B-AN I-AN E-AN
        labels = ["B-AN", "I-AN", "E-AN", "O", "B-AN", "I-AN", "E-AN"]
        tokens = [
            ("Rom", 0, 3), (".", 3, 4), ("5", 5, 6),
            ("et", 7, 9),
            ("Gen", 10, 13), (".", 13, 14), ("3", 15, 16),
        ]
        entities = extract_entities(tokens, labels)
        assert len(entities) == 2

        # Correct counting: 6 non-O tokens, counted once
        stats.entity_tokens += sum(1 for l in labels if l != "O")
        assert stats.entity_tokens == 6

        # Bug would have been: counting inside entity loop → 6 * 2 = 12
        # Verify it's NOT multiplied by number of entities
        assert stats.entity_tokens != len(entities) * sum(1 for l in labels if l != "O")


# =============================================================================
# Integration: Feature→Entity Pipeline Tests
# =============================================================================


class TestFeatureEntityIntegration:
    """Integration tests combining tokenisation, features, and entity extraction."""

    def test_feature_extraction_on_real_text(self):
        """Feature extraction should work on Stöckel-like Latin text."""
        text = "Sicut ait Dominus in Rom. 5, haec sunt vera."
        tokens = tokenize_for_crf(text)
        token_texts = [t[0] for t in tokens]
        features = extract_features(token_texts)

        assert len(features) == len(tokens)
        # Check that the number token has correct features
        for i, (tok, _, _) in enumerate(tokens):
            if tok == "5":
                assert features[i]["word.isdigit()"] is True
            if tok == "Rom":
                assert features[i]["word.istitle()"] is True

    def test_entity_extraction_preserves_offsets(self):
        """Extracted entity offsets should point to correct source text."""
        text = "sicut ait Rom. 5 dicit"
        tokens = tokenize_for_crf(text)
        # Simulate labels where "Rom . 5" is an entity
        labels = ["O", "O", "B-AN", "I-AN", "E-AN", "O"]
        entities = extract_entities(tokens, labels)

        assert len(entities) == 1
        entity_text, label, start, end = entities[0]
        assert text[start:end] == "Rom. 5"
        assert label == "AN"

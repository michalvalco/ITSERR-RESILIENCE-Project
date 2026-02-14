"""Unit tests for the CAS XMI → BIOES converter.

Tests cover the core conversion logic (tokenization, BIOES labelling,
formatting) without requiring dkpro-cassis to be installed — the CAS
integration layer is tested via lightweight mocks.
"""

import pytest
import sys
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "stockel_annotation" / "scripts"))

from cas_to_bioes import (
    tokenize_text,
    assign_bioes_labels,
    format_bioes_output,
    tokens_in_sentence,
    get_annotation_type_label,
    _normalize_label,
    _type_name_to_label,
    ConversionStats,
)


# =============================================================================
# Tokenizer Tests
# =============================================================================


class TestTokenizeText:
    """Tests for the fallback whitespace+punctuation tokenizer."""

    def test_simple_words(self):
        """Simple space-separated words should be tokenized."""
        tokens = tokenize_text("Quod est in")
        assert len(tokens) == 3
        assert tokens[0] == ("Quod", 0, 4)
        assert tokens[1] == ("est", 5, 8)
        assert tokens[2] == ("in", 9, 11)

    def test_punctuation_separated(self):
        """Punctuation should be separate tokens."""
        tokens = tokenize_text("Rom. 5")
        assert len(tokens) == 3
        assert tokens[0] == ("Rom", 0, 3)
        assert tokens[1] == (".", 3, 4)
        assert tokens[2] == ("5", 5, 6)

    def test_multiple_punctuation(self):
        """Multiple punctuation marks should each be a token."""
        tokens = tokenize_text("c. 1.")
        assert len(tokens) == 4
        assert tokens[0] == ("c", 0, 1)
        assert tokens[1] == (".", 1, 2)
        assert tokens[2] == ("1", 3, 4)
        assert tokens[3] == (".", 4, 5)

    def test_empty_string(self):
        """Empty string should return no tokens."""
        tokens = tokenize_text("")
        assert tokens == []

    def test_whitespace_only(self):
        """Whitespace-only string should return no tokens."""
        tokens = tokenize_text("   \t  \n  ")
        assert tokens == []

    def test_section_symbol(self):
        """Section symbol (§) should be a separate token."""
        tokens = tokenize_text("q. 1 § quod")
        assert ("§", 5, 6) in tokens

    def test_preserves_offsets(self):
        """Character offsets should be correct and non-overlapping."""
        text = "Quod est in c. 1."
        tokens = tokenize_text(text)
        for tok_text, start, end in tokens:
            assert text[start:end] == tok_text
            assert start < end

    def test_leading_trailing_whitespace(self):
        """Leading/trailing whitespace should not create tokens."""
        tokens = tokenize_text("  hello world  ")
        assert len(tokens) == 2
        assert tokens[0][0] == "hello"
        assert tokens[1][0] == "world"

    def test_colon_separator(self):
        """Colons used as separators should be tokenized."""
        tokens = tokenize_text("Actor: 20")
        assert len(tokens) == 3
        assert tokens[0] == ("Actor", 0, 5)
        assert tokens[1] == (":", 5, 6)
        assert tokens[2] == ("20", 7, 9)

    def test_semicolon_separator(self):
        """Semicolons should be separate tokens."""
        tokens = tokenize_text("autem;")
        assert len(tokens) == 2
        assert tokens[0] == ("autem", 0, 5)
        assert tokens[1] == (";", 5, 6)


# =============================================================================
# BIOES Label Assignment Tests
# =============================================================================


class TestAssignBioesLabels:
    """Tests for the core BIOES label assignment logic."""

    def test_no_annotations_all_O(self):
        """With no annotations, all tokens should be labelled O."""
        tokens = [("Quod", 0, 4), ("est", 5, 8), ("verum", 9, 14)]
        annotations = []
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["O", "O", "O"]

    def test_single_token_entity_S(self):
        """A single-token annotation should get S- label."""
        tokens = [("non", 0, 3), ("Rom", 4, 7), ("est", 8, 11)]
        annotations = [(4, 7, "BIB")]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["O", "S-BIB", "O"]

    def test_two_token_entity_B_E(self):
        """A two-token annotation should get B- and E- labels."""
        tokens = [("in", 0, 2), ("c", 3, 4), ("1", 5, 6)]
        annotations = [(3, 6, "AN")]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["O", "B-AN", "E-AN"]

    def test_three_token_entity_B_I_E(self):
        """A three-token annotation should get B-, I-, E- labels."""
        tokens = [("in", 0, 2), ("c", 3, 4), (".", 4, 5), ("1", 6, 7)]
        annotations = [(3, 7, "AN")]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["O", "B-AN", "I-AN", "E-AN"]

    def test_multiple_annotations(self):
        """Multiple non-overlapping annotations should each be labelled."""
        tokens = [
            ("Rom", 0, 3), (".", 3, 4), ("5", 5, 6),
            ("et", 7, 9),
            ("Gen", 10, 13), (".", 13, 14), ("3", 15, 16),
        ]
        annotations = [
            (0, 6, "BIB"),    # Rom. 5
            (10, 16, "BIB"),  # Gen. 3
        ]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["B-BIB", "I-BIB", "E-BIB", "O", "B-BIB", "I-BIB", "E-BIB"]

    def test_empty_tokens(self):
        """Empty token list should return empty labels."""
        labels = assign_bioes_labels([], [(0, 5, "AN")])
        assert labels == []

    def test_annotation_no_matching_tokens(self):
        """Annotation span with no overlapping tokens should be ignored."""
        tokens = [("text", 0, 4)]
        annotations = [(10, 15, "AN")]  # no overlap
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["O"]

    def test_partial_overlap(self):
        """Token partially overlapping annotation should be included."""
        tokens = [("word", 3, 7)]
        annotations = [(5, 10, "AN")]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["S-AN"]

    def test_long_multi_token_entity(self):
        """Entity spanning 5+ tokens should have correct B-I-...-I-E pattern."""
        tokens = [
            ("28", 0, 2), (".", 2, 3), ("q", 4, 5),
            (".", 5, 6), ("1", 7, 8), ("§", 9, 10),
            ("quod", 11, 15), ("autem", 16, 21),
        ]
        annotations = [(0, 21, "AN")]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels[0] == "B-AN"
        assert all(l == "I-AN" for l in labels[1:-1])
        assert labels[-1] == "E-AN"

    def test_different_entity_types(self):
        """Different annotation types should produce different labels."""
        tokens = [
            ("Rom", 0, 3), (".", 3, 4), ("5", 5, 6),
            ("Augustinus", 7, 17),
        ]
        annotations = [
            (0, 6, "BIB"),
            (7, 17, "PAT"),
        ]
        labels = assign_bioes_labels(tokens, annotations)
        assert labels == ["B-BIB", "I-BIB", "E-BIB", "S-PAT"]


# =============================================================================
# Sentence Grouping Tests
# =============================================================================


class TestTokensInSentence:
    """Tests for grouping tokens into sentences."""

    def test_all_tokens_in_sentence(self):
        """All tokens within sentence bounds should be included."""
        tokens = [("a", 0, 1), ("b", 2, 3), ("c", 4, 5)]
        indices = tokens_in_sentence(tokens, 0, 10)
        assert indices == [0, 1, 2]

    def test_no_tokens_in_sentence(self):
        """Tokens outside sentence bounds should be excluded."""
        tokens = [("a", 0, 1), ("b", 2, 3)]
        indices = tokens_in_sentence(tokens, 10, 20)
        assert indices == []

    def test_partial_overlap(self):
        """Only tokens whose midpoint is within bounds should be included."""
        tokens = [("a", 0, 2), ("b", 3, 5), ("c", 6, 8)]
        # Sentence covers 3–6, midpoints: a=1, b=4, c=7
        indices = tokens_in_sentence(tokens, 3, 6)
        assert indices == [1]

    def test_adjacent_sentences(self):
        """Tokens should be assigned to correct adjacent sentences."""
        tokens = [("a", 0, 2), ("b", 3, 5), ("c", 6, 8), ("d", 9, 11)]
        sent1 = tokens_in_sentence(tokens, 0, 5)
        sent2 = tokens_in_sentence(tokens, 5, 12)
        assert sent1 == [0, 1]
        assert sent2 == [2, 3]


# =============================================================================
# Formatting Tests
# =============================================================================


class TestFormatBioesOutput:
    """Tests for BIOES output formatting."""

    def test_single_sentence(self):
        """Single sentence should be formatted correctly."""
        sentences = [
            [("Quod", 0, 4, "O"), ("est", 5, 8, "O"), ("in", 9, 11, "B-AN")],
        ]
        output = format_bioes_output(sentences)
        lines = output.strip().split("\n")
        assert len(lines) == 3
        assert lines[0] == "Quod 0 4 O"
        assert lines[1] == "est 5 8 O"
        assert lines[2] == "in 9 11 B-AN"

    def test_multiple_sentences_separated(self):
        """Sentences should be separated by blank lines."""
        sentences = [
            [("Quod", 0, 4, "O")],
            [("Est", 5, 8, "O")],
        ]
        output = format_bioes_output(sentences)
        assert "\n\n" in output

    def test_empty_input(self):
        """Empty sentence list should return empty string."""
        assert format_bioes_output([]) == ""

    def test_output_ends_with_newline(self):
        """Output should end with a newline."""
        sentences = [[("word", 0, 4, "O")]]
        output = format_bioes_output(sentences)
        assert output.endswith("\n")

    def test_bioes_labels_preserved(self):
        """All BIOES label types should appear in output."""
        sentences = [
            [
                ("28", 0, 2, "B-AN"),
                ("q", 3, 4, "I-AN"),
                ("1", 5, 6, "E-AN"),
            ],
            [
                ("Rom", 7, 10, "S-BIB"),
            ],
        ]
        output = format_bioes_output(sentences)
        assert "B-AN" in output
        assert "I-AN" in output
        assert "E-AN" in output
        assert "S-BIB" in output


# =============================================================================
# Label Normalization Tests
# =============================================================================


class TestLabelNormalization:
    """Tests for label normalization functions."""

    def test_gnorm_allegazione(self):
        """'Allegazione normativa' should map to 'AN'."""
        assert _normalize_label("Allegazione normativa") == "AN"

    def test_gnorm_allegazione_with_group(self):
        """'Allegazione normativa[1]' should strip the group suffix."""
        assert _normalize_label("Allegazione normativa[1]") == "AN"

    def test_gnorm_lemma(self):
        """'Lemma glossato' should map to 'LEMMA'."""
        assert _normalize_label("Lemma glossato") == "LEMMA"

    def test_stoeckel_biblical(self):
        """Biblical reference labels should map to 'BIB'."""
        assert _normalize_label("Biblical reference") == "BIB"
        assert _normalize_label("Biblical_Reference") == "BIB"
        assert _normalize_label("BiblicalReference") == "BIB"

    def test_stoeckel_patristic(self):
        """Patristic reference labels should map to 'PAT'."""
        assert _normalize_label("Patristic reference") == "PAT"
        assert _normalize_label("Patristic_Reference") == "PAT"

    def test_stoeckel_reformation(self):
        """Reformation reference labels should map to 'REF'."""
        assert _normalize_label("Reformation reference") == "REF"

    def test_unknown_label_uppercased(self):
        """Unknown labels should be uppercased with spaces → underscores."""
        assert _normalize_label("Custom Label") == "CUSTOM_LABEL"

    def test_type_name_glossa(self):
        """Type name 'Glossa' should map to 'AN'."""
        assert _type_name_to_label("Glossa") == "AN"

    def test_type_name_biblical(self):
        """Type name 'BiblicalReference' should map to 'BIB'."""
        assert _type_name_to_label("BiblicalReference") == "BIB"

    def test_type_name_qualified(self):
        """Qualified type name should use last segment."""
        assert _type_name_to_label("webanno.custom.Glossa") == "AN"


# =============================================================================
# Annotation Type Label Extraction Tests
# =============================================================================


class TestGetAnnotationTypeLabel:
    """Tests for extracting labels from annotation objects."""

    def test_with_explicit_feature(self):
        """Should use explicit type_feature when provided."""

        class MockAnn:
            def get(self, key):
                if key == "Tipo":
                    return "Allegazione normativa"
                return None

        label = get_annotation_type_label(MockAnn(), type_feature="Tipo")
        assert label == "AN"

    def test_auto_detect_tipo(self):
        """Should auto-detect 'Tipo' feature."""

        class MockAnn:
            def get(self, key):
                if key == "Tipo":
                    return "Lemma glossato"
                return None

        label = get_annotation_type_label(MockAnn())
        assert label == "LEMMA"

    def test_auto_detect_value(self):
        """Should auto-detect 'value' feature."""

        class MockAnn:
            def get(self, key):
                if key == "value":
                    return "Biblical reference"
                return None

        label = get_annotation_type_label(MockAnn())
        assert label == "BIB"

    def test_fallback_to_type_name(self):
        """Should fall back to type name when no feature has a value."""

        class MockGlossa:
            def get(self, key):
                return None

        label = get_annotation_type_label(MockGlossa())
        assert label == "MOCKGLOSSA"


# =============================================================================
# ConversionStats Tests
# =============================================================================


class TestConversionStats:
    """Tests for ConversionStats dataclass."""

    def test_default_values(self):
        """ConversionStats should have correct defaults."""
        stats = ConversionStats()
        assert stats.documents_processed == 0
        assert stats.total_tokens == 0
        assert stats.total_annotations == 0
        assert stats.total_sentences == 0
        assert stats.annotations_by_type == {}
        assert stats.documents_skipped == 0


# =============================================================================
# Integration: End-to-End Token→BIOES Tests
# =============================================================================


class TestEndToEndBioes:
    """End-to-end tests combining tokenization, labelling, and formatting."""

    def test_gnorm_example(self):
        """Reproduce the GNORM pipeline example from GNORM_PIPELINE_ANALYSIS.md."""
        # "Quod est in c. 1. § quod autem"
        # Annotations: "c. 1. § quod autem" is annotated as AN
        text = "Quod est in c. 1. § quod autem"
        tokens = tokenize_text(text)
        # c=12-13, .=13-14, 1=15-16, .=16-17, §=18-19, quod=20-24, autem=25-30
        annotations = [(12, 30, "AN")]  # span covering "c. 1. § quod autem"
        labels = assign_bioes_labels(tokens, annotations)

        # Tokens before annotation should be O
        for i, (tok, start, end) in enumerate(tokens):
            if start < 12:
                assert labels[i] == "O", f"Token '{tok}' at {start} should be O"

        # Find annotation tokens
        ann_labels = [
            labels[i] for i, (_, start, end) in enumerate(tokens)
            if start >= 12
        ]
        assert ann_labels[0].startswith("B-")
        assert ann_labels[-1].startswith("E-")
        for mid_label in ann_labels[1:-1]:
            assert mid_label.startswith("I-")

    def test_biblical_reference_example(self):
        """Tag a biblical reference in a Stöckel-like sentence."""
        text = "sicut ait Rom. 5"
        tokens = tokenize_text(text)
        # Rom=10-13, .=13-14, 5=15-16
        annotations = [(10, 16, "BIB")]
        labels = assign_bioes_labels(tokens, annotations)
        formatted = format_bioes_output(
            [[(t[0], t[1], t[2], l) for t, l in zip(tokens, labels)]]
        )
        assert "B-BIB" in formatted
        assert "E-BIB" in formatted
        assert formatted.count("O") == 2  # "sicut" and "ait"

    def test_clustered_references(self):
        """Multiple references in sequence (Stöckel citation cluster)."""
        text = "Actor: 20. 1. Cor: 16."
        tokens = tokenize_text(text)
        # Two annotation spans
        annotations = [
            (0, 10, "BIB"),   # Actor: 20.
            (11, 22, "BIB"),  # 1. Cor: 16.
        ]
        labels = assign_bioes_labels(tokens, annotations)

        # Each span should have its own B...E
        b_count = sum(1 for l in labels if l.startswith("B-"))
        e_count = sum(1 for l in labels if l.startswith("E-"))
        assert b_count == 2
        assert e_count == 2

    def test_roundtrip_format_parse(self):
        """BIOES output should be parseable back to tokens + labels."""
        sentences = [
            [("Rom", 0, 3, "B-BIB"), (".", 3, 4, "I-BIB"), ("5", 5, 6, "E-BIB")],
            [("text", 7, 11, "O")],
        ]
        output = format_bioes_output(sentences)
        parsed_sentences = []
        current_sent = []
        for line in output.strip().split("\n"):
            if line == "":
                if current_sent:
                    parsed_sentences.append(current_sent)
                    current_sent = []
            else:
                parts = line.split()
                assert len(parts) == 4
                current_sent.append(
                    (parts[0], int(parts[1]), int(parts[2]), parts[3])
                )
        if current_sent:
            parsed_sentences.append(current_sent)

        assert len(parsed_sentences) == 2
        assert parsed_sentences[0] == sentences[0]
        assert parsed_sentences[1] == sentences[1]

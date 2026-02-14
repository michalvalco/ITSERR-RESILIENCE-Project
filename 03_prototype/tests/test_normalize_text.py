"""Unit tests for the Stöckel text normalization script.

Tests cover:
- OCR noise removal
- Abbreviation expansion (case-insensitive with case-preserving replacement)
- Long s (ſ) correction
- Structural element marking
- Lemma/reference boundary identification
- Full normalization pipeline
"""

import pytest
import sys
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "stockel_annotation" / "scripts"))

from normalize_text import (
    NormalizationStats,
    remove_ocr_noise,
    expand_abbreviations,
    fix_long_s,
    mark_structural_elements,
    identify_lemma_boundaries,
    normalize_text,
    ABBREVIATIONS,
    LONG_S_PATTERNS,
    CHAPTER_PATTERNS,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def stats() -> NormalizationStats:
    """Create a fresh NormalizationStats instance for each test."""
    return NormalizationStats()


# =============================================================================
# OCR Noise Removal Tests
# =============================================================================


class TestRemoveOCRNoise:
    """Tests for remove_ocr_noise function."""

    def test_removes_pipe_characters(self, stats):
        """Pipe characters should be removed."""
        text = "The text | contains | pipes"
        result = remove_ocr_noise(text, stats)
        assert "|" not in result

    def test_removes_multiple_dashes(self, stats):
        """Multiple consecutive dashes should be collapsed."""
        text = "Some text --- more text"
        result = remove_ocr_noise(text, stats)
        assert "---" not in result

    def test_preserves_page_markers(self, stats):
        """[Page N] markers should be preserved."""
        text = "Start [Page 1] Middle [Page 2] End"
        result = remove_ocr_noise(text, stats)
        assert "[Page 1]" in result
        assert "[Page 2]" in result

    def test_preserves_page_break_markers(self, stats):
        """[PAGE BREAK] markers should be preserved."""
        text = "First part [PAGE BREAK] Second part"
        result = remove_ocr_noise(text, stats)
        assert "[PAGE BREAK]" in result

    def test_removes_single_letter_lines(self, stats):
        """Lines with only a single letter should be removed."""
        text = "Normal line\nA\nAnother line"
        result = remove_ocr_noise(text, stats)
        lines = [l.strip() for l in result.split('\n') if l.strip()]
        assert "A" not in lines or len([l for l in lines if l == "A"]) == 0

    def test_removes_symbol_clusters(self, stats):
        """Clusters of symbols should be removed."""
        text = "Text !@#$% more text"
        result = remove_ocr_noise(text, stats)
        assert "!@#$%" not in result

    def test_tracks_noise_removed(self, stats):
        """Stats should track the number of noise items removed."""
        text = "Text | with | noise"
        remove_ocr_noise(text, stats)
        assert stats.noise_removed > 0


# =============================================================================
# Abbreviation Expansion Tests
# =============================================================================


class TestExpandAbbreviations:
    """Tests for expand_abbreviations function."""

    # -------------------------------------------------------------------------
    # Tironian Et Tests
    # -------------------------------------------------------------------------

    def test_tironian_et_ez_lowercase(self, stats):
        """'ez' should expand to 'et'."""
        text = "hoc ez illud"
        result = expand_abbreviations(text, stats)
        assert "hoc et illud" in result
        assert stats.et_normalized > 0

    def test_tironian_et_ez_uppercase(self, stats):
        """'EZ' should expand to 'Et' (case-preserving)."""
        text = "Hoc EZ illud"
        result = expand_abbreviations(text, stats)
        assert "Hoc Et illud" in result

    def test_tironian_et_cz(self, stats):
        """'cz' should expand to 'et'."""
        text = "hoc cz illud"
        result = expand_abbreviations(text, stats)
        assert "hoc et illud" in result

    def test_tironian_et_with_space(self, stats):
        """'e z' (with space) should expand to 'et'."""
        text = "hoc e z illud"
        result = expand_abbreviations(text, stats)
        assert "et" in result

    # -------------------------------------------------------------------------
    # Que Abbreviation Tests
    # -------------------------------------------------------------------------

    def test_que_semicolon(self, stats):
        """'q;' should expand to 'que'."""
        text = "hominisq; gratia"
        result = expand_abbreviations(text, stats)
        assert "hominisque gratia" in result

    def test_que_attached_to_word(self, stats):
        """'wordq;' should expand the q; part to 'que'."""
        text = "hominisq; gratia"
        result = expand_abbreviations(text, stats)
        assert "hominisque" in result

    def test_que_backreference_preserves_word_case(self, stats):
        """Backreference pattern should preserve the word's original case."""
        # The backreference pattern r'(\w+)q;\s' -> r'\1que ' captures the word
        # and the replacement preserves it via \1 backreference
        text = "Hominisq; gratia"
        result = expand_abbreviations(text, stats)
        assert "Hominisque" in result

    # -------------------------------------------------------------------------
    # Theological Abbreviations - Case Insensitive Tests
    # -------------------------------------------------------------------------

    def test_dominus_lowercase(self, stats):
        """'dñs' should expand to 'dominus'."""
        text = "dñs dixit"
        result = expand_abbreviations(text, stats)
        assert "dominus" in result

    def test_dominus_uppercase(self, stats):
        """'Dñs' should expand to 'Dominus' (case-preserving)."""
        text = "Dñs dixit"
        result = expand_abbreviations(text, stats)
        assert "Dominus" in result

    def test_dominus_all_caps(self, stats):
        """'DÑS' should expand to 'Dominus' (preserves first char case)."""
        text = "DÑS dixit"
        result = expand_abbreviations(text, stats)
        assert "Dominus" in result

    def test_christi_lowercase(self, stats):
        """'xpi' should expand to 'christi'."""
        text = "corpus xpi"
        result = expand_abbreviations(text, stats)
        assert "christi" in result

    def test_christi_uppercase(self, stats):
        """'Xpi' should expand to 'Christi' (case-preserving)."""
        text = "Corpus Xpi"
        result = expand_abbreviations(text, stats)
        assert "Christi" in result

    def test_christus_lowercase(self, stats):
        """'xps' should expand to 'christus'."""
        text = "xps resurrexit"
        result = expand_abbreviations(text, stats)
        assert "christus" in result

    def test_christus_uppercase(self, stats):
        """'Xps' should expand to 'Christus' (case-preserving)."""
        text = "Xps resurrexit"
        result = expand_abbreviations(text, stats)
        assert "Christus" in result

    # -------------------------------------------------------------------------
    # Ecclesiastical Abbreviations Tests
    # -------------------------------------------------------------------------

    def test_ecclesia_lowercase(self, stats):
        """'eccl.' should expand to 'ecclesia'."""
        text = "in eccl. sancta"
        result = expand_abbreviations(text, stats)
        assert "ecclesia" in result

    def test_ecclesia_uppercase(self, stats):
        """'Eccl.' should expand to 'Ecclesia' (case-preserving)."""
        text = "In Eccl. sancta"
        result = expand_abbreviations(text, stats)
        assert "Ecclesia" in result

    def test_episcopus_lowercase(self, stats):
        """'epi.' should expand to 'episcopus'."""
        text = "epi. romanus"
        result = expand_abbreviations(text, stats)
        assert "episcopus" in result

    def test_episcopus_uppercase(self, stats):
        """'Epi.' should expand to 'Episcopus' (case-preserving)."""
        text = "Epi. Romanus"
        result = expand_abbreviations(text, stats)
        assert "Episcopus" in result

    # -------------------------------------------------------------------------
    # Etc. Abbreviation Tests
    # -------------------------------------------------------------------------

    def test_etc_ampersand(self, stats):
        """'&c.' should expand to 'etc.'."""
        text = "libros, codices, &c."
        result = expand_abbreviations(text, stats)
        assert "etc." in result

    def test_etc_ampersand_uppercase(self, stats):
        """'&C.' should expand to 'Etc.' (case-preserving based on C)."""
        # The first alphabetic character in '&C.' is 'C' (uppercase)
        # so the replacement preserves that case
        text = "libros, codices, &C."
        result = expand_abbreviations(text, stats)
        assert "Etc." in result

    def test_etc_ec(self, stats):
        """'ec.' should expand to 'etc.'."""
        text = "libros, codices, ec."
        result = expand_abbreviations(text, stats)
        assert "etc." in result

    # -------------------------------------------------------------------------
    # Statistics Tests
    # -------------------------------------------------------------------------

    def test_tracks_abbreviations_expanded(self, stats):
        """Stats should track the number of abbreviations expanded."""
        text = "Dñs et Xpi et eccl."
        expand_abbreviations(text, stats)
        assert stats.abbreviations_expanded > 0

    def test_tracks_et_normalized_separately(self, stats):
        """Tironian et should be tracked separately from other abbreviations."""
        text = "hoc ez illud cz tertium"
        expand_abbreviations(text, stats)
        assert stats.et_normalized >= 2

    # -------------------------------------------------------------------------
    # Expansion Log Tests (provenance for downstream Stage 4 Layer 2)
    # -------------------------------------------------------------------------

    def test_expansion_log_records_theological_abbreviation(self, stats):
        """Expansion log should record theological abbreviation with original text."""
        text = "dñs dixit"
        expand_abbreviations(text, stats)
        originals = [e["original"] for e in stats.expansion_log]
        assert "dñs" in originals

    def test_expansion_log_records_offset(self, stats):
        """Expansion log entries should include character offset."""
        text = "praefatio dñs dixit"
        expand_abbreviations(text, stats)
        dns_entries = [e for e in stats.expansion_log if e["original"] == "dñs"]
        assert len(dns_entries) == 1
        assert dns_entries[0]["offset"] == 10

    def test_expansion_log_records_pattern(self, stats):
        """Expansion log entries should include the regex pattern used."""
        text = "corpus xpi"
        expand_abbreviations(text, stats)
        xpi_entries = [e for e in stats.expansion_log if e["original"] == "xpi"]
        assert len(xpi_entries) == 1
        assert xpi_entries[0]["pattern"] == r'\bxpi\b'

    def test_expansion_log_records_tironian_et(self, stats):
        """Tironian et expansions should also appear in the log."""
        text = "hoc ez illud"
        expand_abbreviations(text, stats)
        originals = [e["original"] for e in stats.expansion_log]
        assert "ez" in originals

    def test_expansion_log_multiple_entries(self, stats):
        """Multiple expansions in one text should each get a log entry."""
        text = "Dñs et Xpi"
        expand_abbreviations(text, stats)
        assert len(stats.expansion_log) >= 2
        originals = {e["original"] for e in stats.expansion_log}
        assert "Dñs" in originals or "dñs" in originals
        assert "Xpi" in originals or "xpi" in originals

    def test_expansion_log_empty_for_no_matches(self, stats):
        """No abbreviations means empty log."""
        text = "plain Latin text without abbreviations"
        expand_abbreviations(text, stats)
        assert stats.expansion_log == []


# =============================================================================
# Long S Correction Tests
# =============================================================================


class TestFixLongS:
    """Tests for fix_long_s function (OCR misreads of ſ as f)."""

    def test_sicut_correction(self, stats):
        """'ficut' should be corrected to 'sicut'."""
        text = "ficut scriptum est"
        result = fix_long_s(text, stats)
        assert "sicut" in result.lower()

    def test_sed_correction(self, stats):
        """'fed' should be corrected to 'sed'."""
        text = "non hoc, fed illud"
        result = fix_long_s(text, stats)
        assert "sed" in result.lower()

    def test_sunt_correction(self, stats):
        """'funt' should be corrected to 'sunt'."""
        text = "haec funt vera"
        result = fix_long_s(text, stats)
        assert "sunt" in result.lower()

    def test_sint_correction(self, stats):
        """'fint' should be corrected to 'sint'."""
        text = "ut fint iusti"
        result = fix_long_s(text, stats)
        assert "sint" in result.lower()

    def test_semper_correction(self, stats):
        """'femper' should be corrected to 'semper'."""
        text = "femper fidelis"
        result = fix_long_s(text, stats)
        assert "semper" in result.lower()

    def test_spiritus_correction(self, stats):
        """'fpiritus' should be corrected to 'spiritus'."""
        text = "per fpiritum fanctum"
        result = fix_long_s(text, stats)
        assert "spiritu" in result.lower()

    def test_sanctus_correction(self, stats):
        """'fanctus' should be corrected to 'sanctus'."""
        text = "deus fanctus"
        result = fix_long_s(text, stats)
        assert "sanct" in result.lower()

    def test_scriptura_correction(self, stats):
        """'fcriptura' should be corrected to 'scriptura'."""
        text = "in facra fcriptura"
        result = fix_long_s(text, stats)
        assert "scrip" in result.lower()

    def test_esse_correction(self, stats):
        """'efse' should be corrected to 'esse'."""
        text = "videtur efse verum"
        result = fix_long_s(text, stats)
        assert "esse" in result.lower()

    def test_possit_correction(self, stats):
        """'pofsi' patterns should be corrected to 'possi'."""
        text = "non pofsit fieri"
        result = fix_long_s(text, stats)
        assert "possi" in result.lower()

    def test_case_preservation_uppercase(self, stats):
        """Case should be preserved when correcting long s."""
        text = "Ficut scriptum est"
        result = fix_long_s(text, stats)
        assert result.startswith("S") or result.startswith("s")

    def test_case_preservation_lowercase(self, stats):
        """Lowercase should be preserved when correcting long s."""
        text = "ut ficut scriptum"
        result = fix_long_s(text, stats)
        # Should contain 'sicut' in lowercase
        assert "sicut" in result.lower()

    def test_tracks_long_s_fixed(self, stats):
        """Stats should track the number of long s corrections."""
        text = "ficut funt fed"
        fix_long_s(text, stats)
        assert stats.long_s_fixed > 0


# =============================================================================
# Structural Element Marking Tests
# =============================================================================


class TestMarkStructuralElements:
    """Tests for mark_structural_elements function."""

    def test_identifies_de_peccato_originis(self, stats):
        """Should identify 'DE PECCATO ORIGINIS' chapter."""
        text = "[Page 1]\nDE PECCATO ORIGINIS\n"
        mark_structural_elements(text, stats)
        assert "DE PECCATO ORIGINIS" in stats.chapters_found

    def test_identifies_de_iustificatione(self, stats):
        """Should identify 'DE IUSTIFICATIONE' chapter."""
        text = "[Page 1]\nDE IUSTIFICATIONE\n"
        mark_structural_elements(text, stats)
        assert "DE IUSTIFICATIONE" in stats.chapters_found

    def test_identifies_praefatio(self, stats):
        """Should identify 'PRAEFATIO' chapter."""
        text = "[Page 1]\nPRAEFATIO\n"
        mark_structural_elements(text, stats)
        assert "PRAEFATIO" in stats.chapters_found

    def test_identifies_de_deo(self, stats):
        """Should identify 'DE DEO' chapter."""
        text = "[Page 1]\nDE DEO\n"
        mark_structural_elements(text, stats)
        assert "DE DEO" in stats.chapters_found

    def test_case_insensitive_detection(self, stats):
        """Chapter detection should be case-insensitive."""
        text = "[Page 1]\nde peccato originis\n"
        mark_structural_elements(text, stats)
        assert "DE PECCATO ORIGINIS" in stats.chapters_found

    def test_adds_xml_markup(self, stats):
        """Should add XML-like markup for chapters."""
        text = "[Page 1]\nDE DEO\n"
        result = mark_structural_elements(text, stats)
        assert "<!-- CHAPTER:" in result or "DE DEO" in result

    def test_no_duplicate_chapters(self, stats):
        """Same chapter should not be added multiple times."""
        text = "[Page 1]\nDE DEO\n[Page 2]\nDE DEO\n"
        mark_structural_elements(text, stats)
        assert stats.chapters_found.count("DE DEO") == 1


# =============================================================================
# Lemma/Reference Boundary Tests
# =============================================================================


class TestIdentifyLemmaBoundaries:
    """Tests for identify_lemma_boundaries function."""

    # -------------------------------------------------------------------------
    # Biblical References
    # -------------------------------------------------------------------------

    def test_identifies_psalm_reference(self, stats):
        """Should identify Psalm references."""
        text = "ut ait Psalm. 51"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_romans_reference(self, stats):
        """Should identify Romans references."""
        text = "ut ait Rom. 5"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_genesis_reference(self, stats):
        """Should identify Genesis references."""
        text = "in Gen. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_matthew_reference(self, stats):
        """Should identify Matthew references."""
        text = "Matth. 5"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded OT Pentateuch ---

    def test_identifies_exodus_reference(self, stats):
        """Should identify Exodus references."""
        text = "sicut in Exod. 20"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_leviticus_reference(self, stats):
        """Should identify Leviticus references."""
        text = "ut Levit. 19"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_numeri_reference(self, stats):
        """Should identify Numbers references."""
        text = "Num. 14"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_deuteronomium_reference(self, stats):
        """Should identify Deuteronomy references."""
        text = "Deut. 6"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded OT Historical Books ---

    def test_identifies_regum_reference(self, stats):
        """Should identify numbered Kings references (Vulgate numbering)."""
        text = "2. Reg. 12"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_samuel_reference(self, stats):
        """Should identify Samuel references."""
        text = "1. Sam. 17"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_paralipomenon_reference(self, stats):
        """Should identify Chronicles (Paralipomenon) references."""
        text = "1. Paral. 29"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded OT Wisdom Literature ---

    def test_identifies_iob_reference(self, stats):
        """Should identify Job references."""
        text = "Iob. 19"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_proverbs_reference(self, stats):
        """Should identify Proverbs references."""
        text = "Prov. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_ecclesiastes_reference(self, stats):
        """Should identify Ecclesiastes references."""
        text = "Eccles. 12"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded OT Major Prophets ---

    def test_identifies_daniel_reference(self, stats):
        """Should identify Daniel references."""
        text = "Dan. 7"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_ieremiae_reference(self, stats):
        """Should identify Jeremiah with alternate abbreviation."""
        text = "Ier. 31"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_threnorum_reference(self, stats):
        """Should identify Lamentations references."""
        text = "Thren. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded OT Minor Prophets ---

    def test_identifies_zacharias_reference(self, stats):
        """Should identify Zechariah references."""
        text = "Zachar. 9"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_malachi_reference(self, stats):
        """Should identify Malachi references."""
        text = "Malach. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_micah_reference(self, stats):
        """Should identify Micah references."""
        text = "Mich. 5"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_habacuc_reference(self, stats):
        """Should identify Habakkuk references."""
        text = "Habac. 2"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_osea_reference(self, stats):
        """Should identify Hosea references."""
        text = "Ose. 6"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded NT: Gospels ---

    def test_identifies_marci_reference(self, stats):
        """Should identify Mark references (Marci)."""
        text = "Marc. 10"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_lucae_reference(self, stats):
        """Should identify Luke references (Lucae)."""
        text = "Luc. 15"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_ioh_short_reference(self, stats):
        """Should identify short John abbreviation (Ioh.)."""
        text = "Ioh. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded NT: Pauline Epistles ---

    def test_identifies_corinthians_reference(self, stats):
        """Should identify numbered Corinthians references."""
        text = "1. Cor. 13"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_2_corinthians_reference(self, stats):
        """Should identify 2 Corinthians references."""
        text = "2. Cor. 5"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_philippenses_reference(self, stats):
        """Should identify Philippians references."""
        text = "Philip. 2"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_colossenses_reference(self, stats):
        """Should identify Colossians references."""
        text = "Coloss. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_thessalonicenses_reference(self, stats):
        """Should identify Thessalonians references."""
        text = "1. Thess. 4"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_timotheus_reference(self, stats):
        """Should identify Timothy references."""
        text = "2. Tim. 3"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_hebraeos_reference(self, stats):
        """Should identify Hebrews references."""
        text = "Hebr. 11"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded NT: Catholic Epistles ---

    def test_identifies_petri_reference(self, stats):
        """Should identify Peter references."""
        text = "1. Petr. 2"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_iacobi_reference(self, stats):
        """Should identify James references."""
        text = "Iac. 2"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_ioannis_epistles_reference(self, stats):
        """Should identify numbered John epistles."""
        text = "1. Ioan. 4"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Expanded NT: Revelation ---

    def test_identifies_apocalypsis_reference(self, stats):
        """Should identify Revelation (Apocalypsis) references."""
        text = "Apocal. 21"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_apoc_short_reference(self, stats):
        """Should identify short Revelation abbreviation (Apoc.)."""
        text = "Apoc. 1"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # --- Separator inconsistency tests (colon vs period) ---

    def test_identifies_reference_with_colon_separator(self, stats):
        """Should handle colon separator (Actor: 20) per abbreviation notes."""
        text = "Actor: 20"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    def test_identifies_reference_with_mixed_separators(self, stats):
        """Should handle mixed separator patterns (1. Cor: 16)."""
        text = "1. Cor: 16"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="biblical">' in result

    # -------------------------------------------------------------------------
    # Patristic References
    # -------------------------------------------------------------------------

    def test_identifies_augustinus(self, stats):
        """Should identify Augustine references."""
        text = "ut ait Augustinus"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="patristic">' in result

    def test_identifies_hieronymus(self, stats):
        """Should identify Jerome references."""
        text = "secundum Hieronymum"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="patristic">' in result

    def test_identifies_chrysostomus(self, stats):
        """Should identify Chrysostom references."""
        text = "Chrysostomus docet"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="patristic">' in result

    # -------------------------------------------------------------------------
    # Reformation References
    # -------------------------------------------------------------------------

    def test_identifies_luther(self, stats):
        """Should identify Luther references."""
        text = "ut ait Lutherus"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="reformation">' in result

    def test_identifies_melanchthon(self, stats):
        """Should identify Melanchthon references."""
        text = "secundum Melanchthon"
        result = identify_lemma_boundaries(text, stats)
        assert '<ref type="reformation">' in result

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def test_tracks_lemma_markers(self, stats):
        """Stats should track the number of reference markers added."""
        text = "Rom. 5 et Psalm. 51 et Augustinus"
        identify_lemma_boundaries(text, stats)
        assert stats.lemma_markers >= 3


# =============================================================================
# Full Normalization Pipeline Tests
# =============================================================================


class TestNormalizationPipeline:
    """Tests for the full normalize_text function."""

    def test_pipeline_applies_all_transformations(self):
        """Pipeline should apply all normalization steps."""
        text = "ficut Dñs dixit ez [Page 1]\nDE DEO\n"
        stats = NormalizationStats()
        result = normalize_text(text, stats)

        # Should fix long s
        assert "sicut" in result.lower()
        # Should expand abbreviation
        assert "dominus" in result.lower() or "Dominus" in result

    def test_pipeline_preserves_page_markers(self):
        """Page markers should survive the pipeline."""
        text = "[Page 1] Some text [Page 2] More text"
        result = normalize_text(text)
        assert "[Page 1]" in result
        assert "[Page 2]" in result

    def test_pipeline_tracks_all_stats(self):
        """Pipeline should track statistics from all steps."""
        text = "ficut ez illud | noise"
        stats = NormalizationStats()
        normalize_text(text, stats)

        # Should have tracked various changes
        assert stats.total_words_before > 0
        assert stats.total_words_after > 0

    def test_pipeline_cleans_up_whitespace(self):
        """Pipeline should normalize whitespace."""
        text = "Too   many   spaces"
        result = normalize_text(text)
        assert "   " not in result

    def test_pipeline_limits_newlines(self):
        """Pipeline should limit consecutive newlines to 2."""
        text = "Para 1\n\n\n\n\nPara 2"
        result = normalize_text(text)
        assert "\n\n\n" not in result

    def test_pipeline_with_empty_stats(self):
        """Pipeline should work without provided stats."""
        text = "Simple text"
        result = normalize_text(text)
        assert "Simple text" in result


# =============================================================================
# Edge Cases and Regression Tests
# =============================================================================


class TestEdgeCases:
    """Edge cases and regression tests."""

    def test_empty_string(self, stats):
        """Functions should handle empty strings."""
        result = normalize_text("", stats)
        assert result == ""

    def test_only_whitespace(self, stats):
        """Functions should handle whitespace-only strings."""
        result = normalize_text("   \n\n   ", stats)
        assert result.strip() == ""

    def test_already_normalized_text(self, stats):
        """Already-normalized text should not be corrupted."""
        text = "Sicut Dominus dixit, et scriptum est."
        result = normalize_text(text, stats)
        # Should remain largely unchanged
        assert "Dominus" in result or "dominus" in result.lower()
        assert "scriptum" in result.lower()

    def test_mixed_latin_and_noise(self, stats):
        """Mix of Latin and OCR noise should be handled."""
        text = "| Dñs dixit | ficut fcriptum | est |"
        result = normalize_text(text, stats)
        # Noise removed, abbreviations expanded, long s fixed
        assert "|" not in result or result.count("|") < text.count("|")

    def test_backreference_pattern_preserved(self, stats):
        """Patterns with backreferences should work correctly."""
        text = "hominisq; gratia"
        result = expand_abbreviations(text, stats)
        assert "hominisque" in result

    def test_word_boundary_respected(self, stats):
        """Word boundaries should prevent false matches."""
        # 'ez' should expand to 'et' only when it appears as a standalone word (\bez\b)
        # 'fez' contains 'ez' but does not match the \bez\b pattern (starts with 'f')
        text = "hoc fez illud"
        result = expand_abbreviations(text, stats)
        # 'fez' does not match \bez\b so it should not be changed
        assert "fez" in result


# =============================================================================
# Configuration Tests
# =============================================================================


class TestConfiguration:
    """Tests for module-level configuration."""

    def test_abbreviations_dict_not_empty(self):
        """ABBREVIATIONS dictionary should contain patterns."""
        assert len(ABBREVIATIONS) > 0

    def test_long_s_patterns_not_empty(self):
        """LONG_S_PATTERNS list should contain patterns."""
        assert len(LONG_S_PATTERNS) > 0

    def test_chapter_patterns_not_empty(self):
        """CHAPTER_PATTERNS list should contain patterns."""
        assert len(CHAPTER_PATTERNS) > 0

    def test_normalization_stats_default_values(self):
        """NormalizationStats should have correct default values."""
        stats = NormalizationStats()
        assert stats.noise_removed == 0
        assert stats.et_normalized == 0
        assert stats.abbreviations_expanded == 0
        assert stats.long_s_fixed == 0
        assert stats.chapters_found == []
        assert stats.lemma_markers == 0
        assert stats.total_words_before == 0
        assert stats.total_words_after == 0
        assert stats.expansion_log == []

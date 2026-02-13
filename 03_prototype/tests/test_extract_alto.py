"""Unit tests for the ALTO XML → plaintext extraction script.

Tests cover:
- ALTO v2 and v3 namespace parsing
- Hyphenation rejoining (SUBS_TYPE / SUBS_CONTENT)
- Confidence score extraction and CSV output
- Batch processing
- Graceful handling of malformed XML
- Page range filtering
- Text assembly with page/paragraph/line structure
"""

import csv
import logging
import sys
from pathlib import Path

import pytest

# Add the scripts directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "stockel_annotation" / "scripts"))

from extract_alto import (
    _is_encoding_error,
    assemble_text,
    collect_word_confidence,
    compute_stats,
    detect_namespace,
    extract_confidence_from_alto,
    extract_text_from_alto,
    main,
    parse_alto_file,
    parse_page_range,
    process_batch,
    write_confidence_csv,
)
from lxml import etree


# =============================================================================
# ALTO XML Fixtures
# =============================================================================

ALTO_V3_BASIC = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1" WIDTH="2480" HEIGHT="3508">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String ID="s1" CONTENT="De" WC="0.95" HPOS="100" VPOS="200"/>
            <SP/>
            <String ID="s2" CONTENT="Peccato" WC="0.92" HPOS="200" VPOS="200"/>
          </TextLine>
          <TextLine ID="line_2">
            <String ID="s3" CONTENT="Caput" WC="0.97" HPOS="100" VPOS="280"/>
            <SP/>
            <String ID="s4" CONTENT="I." WC="0.99" HPOS="200" VPOS="280"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_V2_BASIC = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v2#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="Sicut" WC="0.90"/>
            <SP/>
            <String CONTENT="scriptum" WC="0.85"/>
            <SP/>
            <String CONTENT="est" WC="0.98"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_NO_NAMESPACE = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto>
  <Layout>
    <Page ID="page_1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="sine" WC="0.91"/>
            <SP/>
            <String CONTENT="nomine" WC="0.88"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_HYPHENATION = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="De" WC="0.95"/>
            <SP/>
            <String CONTENT="Peccato" WC="0.92"/>
            <SP/>
            <String CONTENT="Origi" WC="0.88"
                    SUBS_TYPE="HypPart1" SUBS_CONTENT="Originali"/>
            <HYP CONTENT="-"/>
          </TextLine>
          <TextLine ID="line_2">
            <String CONTENT="nali" WC="0.88"
                    SUBS_TYPE="HypPart2" SUBS_CONTENT="Originali"/>
            <SP/>
            <String CONTENT="Caput" WC="0.97"/>
            <SP/>
            <String CONTENT="I." WC="0.99"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_MULTI_PAGE = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="Page" WC="0.95"/>
            <SP/>
            <String CONTENT="one" WC="0.93"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
    <Page ID="page_2" PHYSICAL_IMG_NR="2">
      <PrintSpace>
        <TextBlock ID="block_2">
          <TextLine ID="line_2">
            <String CONTENT="Page" WC="0.96"/>
            <SP/>
            <String CONTENT="two" WC="0.94"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
    <Page ID="page_3" PHYSICAL_IMG_NR="3">
      <PrintSpace>
        <TextBlock ID="block_3">
          <TextLine ID="line_3">
            <String CONTENT="Page" WC="0.91"/>
            <SP/>
            <String CONTENT="three" WC="0.89"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_MULTI_BLOCK = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="First" WC="0.95"/>
            <SP/>
            <String CONTENT="paragraph." WC="0.93"/>
          </TextLine>
        </TextBlock>
        <TextBlock ID="block_2">
          <TextLine ID="line_2">
            <String CONTENT="Second" WC="0.96"/>
            <SP/>
            <String CONTENT="paragraph." WC="0.94"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_LOW_CONFIDENCE = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="clear" WC="0.95"/>
            <SP/>
            <String CONTENT="garbled" WC="0.30"/>
            <SP/>
            <String CONTENT="text" WC="0.45"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_MISSING_CONTENT = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="good" WC="0.95"/>
            <SP/>
            <String WC="0.50"/>
            <SP/>
            <String CONTENT="word" WC="0.90"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""

ALTO_HYPHENATION_NO_SUBS_CONTENT = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1" PHYSICAL_IMG_NR="1">
      <PrintSpace>
        <TextBlock ID="block_1">
          <TextLine ID="line_1">
            <String CONTENT="Origi" WC="0.88"
                    SUBS_TYPE="HypPart1"/>
            <HYP CONTENT="-"/>
          </TextLine>
          <TextLine ID="line_2">
            <String CONTENT="nali" WC="0.88"
                    SUBS_TYPE="HypPart2"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""


# =============================================================================
# Helper: write XML string to a temporary file
# =============================================================================

@pytest.fixture
def alto_file(tmp_path):
    """Factory fixture: write ALTO XML content to a temp file and return its path."""
    def _write(content: str, name: str = "test.xml") -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p
    return _write


# =============================================================================
# Namespace Detection Tests
# =============================================================================


class TestNamespaceDetection:
    """Tests for detect_namespace function."""

    def test_detects_v3_namespace(self):
        """Should detect ALTO v3 namespace."""
        tree = etree.ElementTree(etree.fromstring(ALTO_V3_BASIC.encode()))
        ns = detect_namespace(tree)
        assert ns == "http://www.loc.gov/standards/alto/ns-v3#"

    def test_detects_v2_namespace(self):
        """Should detect ALTO v2 namespace."""
        tree = etree.ElementTree(etree.fromstring(ALTO_V2_BASIC.encode()))
        ns = detect_namespace(tree)
        assert ns == "http://www.loc.gov/standards/alto/ns-v2#"

    def test_detects_no_namespace(self):
        """Should return None for ALTO without namespace."""
        tree = etree.ElementTree(etree.fromstring(ALTO_NO_NAMESPACE.encode()))
        ns = detect_namespace(tree)
        assert ns is None


# =============================================================================
# Basic Parsing Tests
# =============================================================================


class TestBasicParsing:
    """Tests for parsing ALTO XML into structured data."""

    def test_parse_v3_basic(self, alto_file):
        """Should parse ALTO v3 XML correctly."""
        path = alto_file(ALTO_V3_BASIC)
        pages, ns = parse_alto_file(path)
        assert len(pages) == 1
        assert ns == "http://www.loc.gov/standards/alto/ns-v3#"
        # One block with two lines
        assert len(pages[0]) == 1
        assert len(pages[0][0]) == 2

    def test_parse_v2_basic(self, alto_file):
        """Should parse ALTO v2 XML correctly."""
        path = alto_file(ALTO_V2_BASIC)
        pages, ns = parse_alto_file(path)
        assert len(pages) == 1
        assert ns == "http://www.loc.gov/standards/alto/ns-v2#"

    def test_parse_no_namespace(self, alto_file):
        """Should parse ALTO without namespace."""
        path = alto_file(ALTO_NO_NAMESPACE)
        pages, ns = parse_alto_file(path)
        assert len(pages) == 1
        assert ns is None
        # Check words extracted
        words = pages[0][0][0]
        assert words[0].content == "sine"
        assert words[1].content == "nomine"

    def test_parse_multi_page(self, alto_file):
        """Should parse multi-page ALTO files."""
        path = alto_file(ALTO_MULTI_PAGE)
        pages, _ = parse_alto_file(path)
        assert len(pages) == 3

    def test_parse_word_confidence(self, alto_file):
        """Should extract WC confidence values."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        first_word = pages[0][0][0][0]
        assert first_word.content == "De"
        assert first_word.confidence == pytest.approx(0.95)

    def test_parse_missing_content_attribute(self, alto_file):
        """Should skip String elements missing CONTENT attribute."""
        path = alto_file(ALTO_MISSING_CONTENT)
        pages, _ = parse_alto_file(path)
        words = pages[0][0][0]
        # Should have 2 words, skipping the one with no CONTENT
        assert len(words) == 2
        assert words[0].content == "good"
        assert words[1].content == "word"


# =============================================================================
# Text Assembly Tests
# =============================================================================


class TestTextAssembly:
    """Tests for assembling plaintext from parsed ALTO data."""

    def test_basic_assembly(self, alto_file):
        """Should assemble text with page markers and line breaks."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        assert "[Page 1]" in text
        assert "De Peccato" in text
        assert "Caput I." in text

    def test_multi_page_assembly(self, alto_file):
        """Should separate pages with [PAGE BREAK] markers."""
        path = alto_file(ALTO_MULTI_PAGE)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        assert "[Page 1]" in text
        assert "[PAGE BREAK]" in text
        assert "[Page 2]" in text
        assert "[Page 3]" in text
        assert "Page one" in text
        assert "Page two" in text
        assert "Page three" in text

    def test_paragraph_separation(self, alto_file):
        """TextBlocks should be separated by a blank line."""
        path = alto_file(ALTO_MULTI_BLOCK)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        # Two blocks should be separated by blank line
        assert "First paragraph.\n\nSecond paragraph." in text

    def test_line_breaks_within_block(self, alto_file):
        """TextLines within a block should be separated by newlines."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        assert "De Peccato\nCaput I." in text

    def test_empty_pages_produces_empty_string(self):
        """Assembling no pages should return empty string."""
        assert assemble_text([]) == ""


# =============================================================================
# Hyphenation Tests
# =============================================================================


class TestHyphenation:
    """Tests for hyphenated word rejoining."""

    def test_hyphenation_with_subs_content(self, alto_file):
        """Should rejoin hyphenated words using SUBS_CONTENT."""
        path = alto_file(ALTO_HYPHENATION)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        # "Origi-" + "nali" should become "Originali" from SUBS_CONTENT
        assert "Originali" in text
        # The separate parts should not appear
        assert "Origi " not in text
        assert " nali" not in text

    def test_hyphenation_expected_output(self, alto_file):
        """Full output should match expected format from spec."""
        path = alto_file(ALTO_HYPHENATION)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        assert "De Peccato Originali" in text
        assert "Caput I." in text

    def test_hyphenation_without_subs_content(self, alto_file):
        """Should fall back to raw CONTENT when SUBS_CONTENT is missing."""
        path = alto_file(ALTO_HYPHENATION_NO_SUBS_CONTENT)
        pages, _ = parse_alto_file(path)
        text = assemble_text(pages)
        # Without SUBS_CONTENT, HypPart1 uses its raw CONTENT
        assert "Origi" in text
        # HypPart2 is still skipped because HypPart1 was present
        assert "nali" not in text

    def test_orphaned_hyppart2_emits_content(self):
        """Orphaned HypPart2 (no preceding HypPart1) should emit its content."""
        from extract_alto import WordInfo, _assemble_block
        # Simulate a block whose first line starts with an orphaned HypPart2
        # (e.g., page-range extraction that starts mid-hyphenation)
        lines = [[
            WordInfo(content="nali", confidence=0.88, page=2, line_id="l1",
                     subs_type="HypPart2", subs_content="Originali"),
            WordInfo(content="Caput", confidence=0.97, page=2, line_id="l1"),
        ]]
        result = _assemble_block(lines)
        assert "nali" in result[0]
        assert "Caput" in result[0]


# =============================================================================
# Confidence Score Tests
# =============================================================================


class TestConfidenceScores:
    """Tests for confidence score extraction."""

    def test_collect_confidence_data(self, alto_file):
        """Should collect per-word confidence data."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        rows = collect_word_confidence(pages)
        assert len(rows) == 4  # 4 words
        assert rows[0]["word"] == "De"
        assert rows[0]["confidence"] == pytest.approx(0.95)
        assert rows[0]["page"] == 1

    def test_confidence_csv_output(self, alto_file, tmp_path):
        """Should write valid CSV with confidence data."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        rows = collect_word_confidence(pages)

        csv_path = tmp_path / "confidence.csv"
        write_confidence_csv(rows, csv_path)

        assert csv_path.exists()
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            csv_rows = list(reader)
        assert len(csv_rows) == 4
        assert csv_rows[0]["word"] == "De"
        assert float(csv_rows[0]["confidence"]) == pytest.approx(0.95)

    def test_low_confidence_detection(self, alto_file):
        """Should detect words below confidence threshold."""
        path = alto_file(ALTO_LOW_CONFIDENCE)
        pages, _ = parse_alto_file(path)
        stats = compute_stats(pages, confidence_threshold=0.7)
        assert stats.words_below_threshold == 2  # "garbled" (0.30) and "text" (0.45)

    def test_page_review_flagging(self, alto_file):
        """Should flag pages with mean confidence below threshold."""
        path = alto_file(ALTO_LOW_CONFIDENCE)
        pages, _ = parse_alto_file(path)
        stats = compute_stats(pages, confidence_threshold=0.7)
        # Mean of (0.95, 0.30, 0.45) ≈ 0.567 < 0.7
        assert 1 in stats.pages_needing_review


# =============================================================================
# Statistics Tests
# =============================================================================


class TestStatistics:
    """Tests for extraction statistics computation."""

    def test_total_pages(self, alto_file):
        """Should count total pages."""
        path = alto_file(ALTO_MULTI_PAGE)
        pages, _ = parse_alto_file(path)
        stats = compute_stats(pages)
        assert stats.total_pages == 3

    def test_total_words(self, alto_file):
        """Should count total words."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        stats = compute_stats(pages)
        assert stats.total_words == 4

    def test_mean_confidence(self, alto_file):
        """Should compute mean confidence correctly."""
        path = alto_file(ALTO_V3_BASIC)
        pages, _ = parse_alto_file(path)
        stats = compute_stats(pages)
        expected_mean = (0.95 + 0.92 + 0.97 + 0.99) / 4
        actual_mean = stats.total_confidence_sum / stats.words_with_confidence
        assert actual_mean == pytest.approx(expected_mean)


# =============================================================================
# Page Range Filtering Tests
# =============================================================================


class TestPageRangeFiltering:
    """Tests for page range selection."""

    def test_filter_single_page(self, alto_file):
        """Should extract only the specified page."""
        path = alto_file(ALTO_MULTI_PAGE)
        pages, _ = parse_alto_file(path, page_range=(2, 2))
        assert len(pages) == 1
        text = assemble_text(pages, page_offset=1)
        assert "Page two" in text
        assert "Page one" not in text

    def test_filter_page_range(self, alto_file):
        """Should extract pages within the specified range."""
        path = alto_file(ALTO_MULTI_PAGE)
        pages, _ = parse_alto_file(path, page_range=(1, 2))
        assert len(pages) == 2
        text = assemble_text(pages)
        assert "Page one" in text
        assert "Page two" in text
        assert "Page three" not in text

    def test_filter_preserves_page_numbers(self, alto_file):
        """Page markers should use correct page numbers with page_range."""
        path = alto_file(ALTO_MULTI_PAGE)
        pages, _ = parse_alto_file(path, page_range=(2, 3))
        text = assemble_text(pages, page_offset=1)
        assert "[Page 2]" in text
        assert "[Page 3]" in text
        assert "[Page 1]" not in text

    def test_parse_page_range_string(self):
        """Should parse page range strings correctly."""
        assert parse_page_range("1-10") == (1, 10)
        assert parse_page_range("5") == (5, 5)

    def test_parse_page_range_invalid(self):
        """Should raise ValueError for invalid page ranges."""
        with pytest.raises(ValueError):
            parse_page_range("10-5")  # start > end
        with pytest.raises(ValueError):
            parse_page_range("0-5")  # start < 1


# =============================================================================
# Malformed XML Tests
# =============================================================================


class TestMalformedXML:
    """Tests for graceful handling of malformed or unusual XML."""

    def test_empty_page(self, alto_file):
        """Should handle pages with no text content."""
        xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1"/>
  </Layout>
</alto>
"""
        path = alto_file(xml)
        pages, _ = parse_alto_file(path)
        assert len(pages) == 1
        assert len(pages[0]) == 0  # No blocks

    def test_malformed_xml_raises(self, alto_file):
        """Should raise XMLSyntaxError for completely broken XML."""
        path = alto_file("<not-xml!!!>>>>>")
        with pytest.raises(etree.XMLSyntaxError):
            parse_alto_file(path)

    def test_no_pages_element(self, alto_file):
        """Should handle ALTO with no Page elements."""
        xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout/>
</alto>
"""
        path = alto_file(xml)
        pages, _ = parse_alto_file(path)
        assert len(pages) == 0

    def test_invalid_confidence_value(self, alto_file):
        """Should handle non-numeric WC values gracefully."""
        xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1">
      <PrintSpace>
        <TextBlock ID="b1">
          <TextLine ID="l1">
            <String CONTENT="word" WC="invalid"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""
        path = alto_file(xml)
        pages, _ = parse_alto_file(path)
        word = pages[0][0][0][0]
        assert word.content == "word"
        assert word.confidence is None  # Gracefully set to None

    def test_latin1_fallback(self, tmp_path):
        """Should handle Latin-1 encoded files."""
        xml_content = '<?xml version="1.0" encoding="ISO-8859-1"?>\n<alto><Layout><Page ID="p1"><PrintSpace><TextBlock ID="b1"><TextLine ID="l1"><String CONTENT="caf\xe9" WC="0.9"/></TextLine></TextBlock></PrintSpace></Page></Layout></alto>'
        path = tmp_path / "latin1.xml"
        path.write_bytes(xml_content.encode("latin-1"))
        pages, _ = parse_alto_file(path)
        assert len(pages) == 1
        assert pages[0][0][0][0].content == "café"


# =============================================================================
# Batch Processing Tests
# =============================================================================


class TestBatchProcessing:
    """Tests for batch directory processing."""

    def test_batch_basic(self, tmp_path):
        """Should process a directory of ALTO XML files."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        # Write two ALTO files
        (input_dir / "file1.xml").write_text(ALTO_V3_BASIC, encoding="utf-8")
        (input_dir / "file2.xml").write_text(ALTO_V2_BASIC, encoding="utf-8")

        process_batch(input_dir, output_dir)

        assert (output_dir / "file1.txt").exists()
        assert (output_dir / "file2.txt").exists()

        text1 = (output_dir / "file1.txt").read_text(encoding="utf-8")
        assert "De Peccato" in text1

        text2 = (output_dir / "file2.txt").read_text(encoding="utf-8")
        assert "Sicut scriptum est" in text2

    def test_batch_recursive(self, tmp_path):
        """Should process nested subdirectories with --recursive."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        sub = input_dir / "subdir"
        sub.mkdir(parents=True)

        (input_dir / "top.xml").write_text(ALTO_V3_BASIC, encoding="utf-8")
        (sub / "nested.xml").write_text(ALTO_V2_BASIC, encoding="utf-8")

        process_batch(input_dir, output_dir, recursive=True)

        assert (output_dir / "top.txt").exists()
        assert (output_dir / "subdir" / "nested.txt").exists()

    def test_batch_empty_directory(self, tmp_path):
        """Should handle empty input directory gracefully."""
        input_dir = tmp_path / "empty"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        # Should not raise
        process_batch(input_dir, output_dir)
        assert not output_dir.exists()

    def test_batch_skips_malformed(self, tmp_path):
        """Should skip malformed XML files and continue."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        (input_dir / "good.xml").write_text(ALTO_V3_BASIC, encoding="utf-8")
        (input_dir / "bad.xml").write_text("<broken!!!>", encoding="utf-8")

        process_batch(input_dir, output_dir)

        assert (output_dir / "good.txt").exists()
        # bad.txt should NOT exist because the XML was malformed
        assert not (output_dir / "bad.txt").exists()

    def test_batch_confidence_csv(self, tmp_path):
        """Should generate confidence CSVs in batch mode."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        (input_dir / "file1.xml").write_text(ALTO_V3_BASIC, encoding="utf-8")

        process_batch(input_dir, output_dir, confidence_csv=True)

        assert (output_dir / "file1.txt").exists()
        assert (output_dir / "file1.confidence.csv").exists()


# =============================================================================
# Public API Tests
# =============================================================================


class TestPublicAPI:
    """Tests for the public Python API functions."""

    def test_extract_text_from_alto(self, alto_file):
        """extract_text_from_alto should return plaintext string."""
        path = alto_file(ALTO_V3_BASIC)
        text = extract_text_from_alto(path)
        assert isinstance(text, str)
        assert "De Peccato" in text

    def test_extract_text_with_page_range(self, alto_file):
        """extract_text_from_alto should respect page_range."""
        path = alto_file(ALTO_MULTI_PAGE)
        text = extract_text_from_alto(path, page_range=(2, 2))
        assert "Page two" in text
        assert "Page one" not in text

    def test_extract_confidence_from_alto(self, alto_file):
        """extract_confidence_from_alto should return list of dicts."""
        path = alto_file(ALTO_V3_BASIC)
        rows = extract_confidence_from_alto(path)
        assert len(rows) == 4
        assert all("word" in r and "confidence" in r for r in rows)

    def test_string_path_accepted(self, alto_file):
        """API should accept string paths as well as Path objects."""
        path = alto_file(ALTO_V3_BASIC)
        text = extract_text_from_alto(str(path))
        assert "De Peccato" in text


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """End-to-end integration tests."""

    def test_full_extraction_matches_expected(self, alto_file):
        """Verify the full sample from the spec produces expected output."""
        path = alto_file(ALTO_HYPHENATION)
        text = extract_text_from_alto(path)

        # Should contain page marker
        assert "[Page 1]" in text
        # Hyphenated word should be rejoined
        assert "De Peccato Originali" in text
        assert "Caput I." in text
        # Should not contain broken parts
        assert "Origi " not in text

    def test_output_compatible_with_normalize(self, alto_file):
        """Output should use markers compatible with normalize_text.py."""
        path = alto_file(ALTO_MULTI_PAGE)
        text = extract_text_from_alto(path)
        # normalize_text.py protects [Page N] and [PAGE BREAK] markers
        assert "[Page 1]" in text
        assert "[PAGE BREAK]" in text


# =============================================================================
# Encoding Error Detection Tests
# =============================================================================


class TestIsEncodingError:
    """Tests for the _is_encoding_error heuristic."""

    def test_detects_encoding_error_message(self):
        """Should detect messages containing 'encoding error'."""
        err = etree.XMLSyntaxError("encoding error: output conversion failed", 0, 0, 0)
        assert _is_encoding_error(err) is True

    def test_detects_bytes_cannot_be_decoded(self):
        """Should detect 'bytes cannot be decoded' variant."""
        err = etree.XMLSyntaxError("input bytes cannot be decoded", 0, 0, 0)
        assert _is_encoding_error(err) is True

    def test_detects_bytes_can_not_be_decoded(self):
        """Should detect 'bytes can not be decoded' variant (alternate spelling)."""
        err = etree.XMLSyntaxError("bytes can not be decoded using encoding", 0, 0, 0)
        assert _is_encoding_error(err) is True

    def test_detects_invalid_byte(self):
        """Should detect 'invalid byte' messages."""
        err = etree.XMLSyntaxError("invalid byte sequence", 0, 0, 0)
        assert _is_encoding_error(err) is True

    def test_rejects_non_encoding_error(self):
        """Should return False for non-encoding XML errors."""
        err = etree.XMLSyntaxError("Opening and ending tag mismatch", 0, 0, 0)
        assert _is_encoding_error(err) is False

    def test_rejects_generic_syntax_error(self):
        """Should return False for generic XML syntax errors."""
        err = etree.XMLSyntaxError("StartTag: invalid element name", 0, 0, 0)
        assert _is_encoding_error(err) is False


# =============================================================================
# CLI Flag Regression Tests
# =============================================================================


class TestCLIBatchConfidenceFlags:
    """Regression tests for --confidence vs --export-confidence in batch mode."""

    def test_confidence_flag_does_not_create_csv_in_batch(self, tmp_path, caplog):
        """--confidence path should be ignored in batch mode (no CSV created)."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()
        (input_dir / "file1.xml").write_text(ALTO_V3_BASIC, encoding="utf-8")

        csv_path = tmp_path / "should_not_exist.csv"
        sys.argv = [
            "extract_alto",
            str(input_dir),
            "-o", str(output_dir),
            "--confidence", str(csv_path),
        ]

        with caplog.at_level(logging.WARNING):
            main()

        # The CSV specified by --confidence should NOT be created
        assert not csv_path.exists()
        # No per-file confidence CSVs should exist either
        assert not list(output_dir.glob("*.confidence.csv"))
        # Should warn the user
        assert "--confidence" in caplog.text

    def test_export_confidence_creates_csv_in_batch(self, tmp_path):
        """--export-confidence should create per-file CSVs in batch mode."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()
        (input_dir / "file1.xml").write_text(ALTO_V3_BASIC, encoding="utf-8")

        sys.argv = [
            "extract_alto",
            str(input_dir),
            "-o", str(output_dir),
            "--export-confidence",
        ]
        main()

        assert (output_dir / "file1.txt").exists()
        assert (output_dir / "file1.confidence.csv").exists()


class TestCLISingleFileExportConfidence:
    """Tests for --export-confidence warning in single-file mode."""

    def test_export_confidence_warns_in_single_file_mode(self, alto_file, tmp_path, caplog):
        """--export-confidence in single-file mode should emit a warning."""
        path = alto_file(ALTO_V3_BASIC)
        out = tmp_path / "output.txt"

        sys.argv = [
            "extract_alto",
            str(path),
            "-o", str(out),
            "--export-confidence",
        ]

        with caplog.at_level(logging.WARNING):
            main()

        # Output text should still be generated
        assert out.exists()
        assert "De Peccato" in out.read_text(encoding="utf-8")
        # Should warn that --export-confidence is for batch mode
        assert "--export-confidence" in caplog.text
        # No CSV should be generated (no --confidence path was provided)
        assert not list(tmp_path.glob("*.csv"))

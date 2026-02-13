"""Unit tests for the OCR processor script.

Tests cover:
- Backward compatibility (--format txt produces same output as before)
- ALTO XML extraction (--format alto calls image_to_alto_xml, writes .xml)
- Dual output (--format both produces .txt and .xml)
- ALTO output directory creation
- clean_ocr_text() is NOT applied to ALTO output
- Version guard for image_to_alto_xml

All heavy dependencies (pytesseract, pdf2image) are mocked so tests run
without a Tesseract installation.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add the scripts directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "stockel_annotation" / "scripts"))

from ocr_processor import (
    clean_ocr_text,
    extract_alto_from_pdf,
    extract_both_from_pdf,
    extract_text_from_pdf,
    identify_chapters,
    main,
    save_alto,
    save_text,
)


# =============================================================================
# Fixtures
# =============================================================================


SAMPLE_OCR_TEXT = "De Peccato Originali\nCaput I.\n"
SAMPLE_ALTO_XML = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
  <Layout>
    <Page ID="page_1">
      <PrintSpace>
        <TextBlock ID="b1">
          <TextLine ID="l1">
            <String CONTENT="De" WC="0.95"/>
          </TextLine>
        </TextBlock>
      </PrintSpace>
    </Page>
  </Layout>
</alto>
"""


@pytest.fixture
def mock_pdf_pages():
    """Create mock PIL Image objects representing PDF pages."""
    page1 = MagicMock(name="Page1Image")
    page2 = MagicMock(name="Page2Image")
    return [page1, page2]


@pytest.fixture
def mock_convert(mock_pdf_pages):
    """Patch pdf2image.convert_from_path to return mock pages."""
    with patch("ocr_processor.convert_from_path", return_value=mock_pdf_pages) as m:
        yield m


@pytest.fixture
def mock_tesseract():
    """Patch pytesseract functions to return sample data."""
    with patch("ocr_processor.pytesseract") as mock_pt:
        mock_pt.image_to_string.return_value = SAMPLE_OCR_TEXT
        mock_pt.image_to_alto_xml.return_value = SAMPLE_ALTO_XML
        mock_pt.get_tesseract_version.return_value = "5.3.0"
        yield mock_pt


# =============================================================================
# Text Cleaning Tests
# =============================================================================


class TestCleanOCRText:
    """Tests for the clean_ocr_text function."""

    def test_normalizes_long_s(self):
        """Should replace ſ with s."""
        assert "s" in clean_ocr_text("ſ")
        assert "ſ" not in clean_ocr_text("ſicut")

    def test_normalizes_ligatures(self):
        """Should expand ligature characters."""
        assert clean_ocr_text("ﬁrst") == "first"
        assert clean_ocr_text("ﬂow") == "flow"

    def test_normalizes_whitespace(self):
        """Should collapse multiple spaces."""
        result = clean_ocr_text("too   many   spaces")
        assert "   " not in result

    def test_limits_newlines(self):
        """Should limit consecutive newlines to 2."""
        result = clean_ocr_text("para1\n\n\n\n\npara2")
        assert "\n\n\n" not in result

    def test_strips_line_whitespace(self):
        """Should strip leading/trailing whitespace from lines."""
        result = clean_ocr_text("  hello  \n  world  ")
        lines = result.split("\n")
        assert all(line == line.strip() for line in lines)

    def test_vu_confusion(self):
        """Should fix v/u confusion in Latin."""
        assert "un" in clean_ocr_text("vn")
        assert "quod" in clean_ocr_text("qvod")


# =============================================================================
# Chapter Identification Tests
# =============================================================================


class TestIdentifyChapters:
    """Tests for chapter identification."""

    def test_finds_de_peccato(self):
        """Should find DE PECCATO ORIG pattern."""
        chapters = identify_chapters("text DE PECCATO ORIGINIS more text")
        assert len(chapters) > 0

    def test_case_insensitive(self):
        """Should match case-insensitively."""
        chapters = identify_chapters("de peccato originis")
        assert len(chapters) > 0

    def test_no_match(self):
        """Should return empty dict when no chapters found."""
        chapters = identify_chapters("just some random latin text")
        assert len(chapters) == 0


# =============================================================================
# Text Extraction Tests (mocked)
# =============================================================================


class TestExtractTextFromPDF:
    """Tests for extract_text_from_pdf with mocked dependencies."""

    def test_returns_dict_of_page_texts(self, mock_convert, mock_tesseract):
        """Should return dict mapping page numbers to text."""
        result = extract_text_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert 1 in result
        assert 2 in result
        assert result[1] == SAMPLE_OCR_TEXT

    def test_calls_image_to_string(self, mock_convert, mock_tesseract):
        """Should call pytesseract.image_to_string for each page."""
        extract_text_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert mock_tesseract.image_to_string.call_count == 2

    def test_does_not_call_alto(self, mock_convert, mock_tesseract):
        """Should NOT call image_to_alto_xml."""
        extract_text_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        mock_tesseract.image_to_alto_xml.assert_not_called()

    def test_passes_latin_language(self, mock_convert, mock_tesseract):
        """Should pass lang='lat' to pytesseract."""
        extract_text_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        call_kwargs = mock_tesseract.image_to_string.call_args
        assert call_kwargs[1]["lang"] == "lat"


# =============================================================================
# ALTO Extraction Tests (mocked)
# =============================================================================


class TestExtractAltoFromPDF:
    """Tests for extract_alto_from_pdf with mocked dependencies."""

    def test_returns_dict_of_alto_bytes(self, mock_convert, mock_tesseract):
        """Should return dict mapping page numbers to ALTO XML bytes."""
        result = extract_alto_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert isinstance(result[1], bytes)
        assert b"<alto" in result[1]

    def test_calls_image_to_alto_xml(self, mock_convert, mock_tesseract):
        """Should call pytesseract.image_to_alto_xml for each page."""
        extract_alto_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert mock_tesseract.image_to_alto_xml.call_count == 2

    def test_does_not_call_image_to_string(self, mock_convert, mock_tesseract):
        """Should NOT call image_to_string."""
        extract_alto_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        mock_tesseract.image_to_string.assert_not_called()


# =============================================================================
# Both Extraction Tests (mocked)
# =============================================================================


class TestExtractBothFromPDF:
    """Tests for extract_both_from_pdf with mocked dependencies."""

    def test_returns_both_dicts(self, mock_convert, mock_tesseract):
        """Should return tuple of (text_dict, alto_dict)."""
        texts, altos = extract_both_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert len(texts) == 2
        assert len(altos) == 2
        assert isinstance(texts[1], str)
        assert isinstance(altos[1], bytes)

    def test_calls_both_pytesseract_functions(self, mock_convert, mock_tesseract):
        """Should call both image_to_string and image_to_alto_xml."""
        extract_both_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert mock_tesseract.image_to_string.call_count == 2
        assert mock_tesseract.image_to_alto_xml.call_count == 2

    def test_single_pdf_conversion(self, mock_convert, mock_tesseract):
        """Should convert PDF to images only once."""
        extract_both_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        assert mock_convert.call_count == 1


# =============================================================================
# Output Tests
# =============================================================================


class TestSaveText:
    """Tests for save_text function."""

    def test_writes_file_with_header(self, tmp_path, mock_tesseract):
        """Should write text with metadata header."""
        out = tmp_path / "output.txt"
        save_text("Hello world", out, {"Page": 1})
        content = out.read_text(encoding="utf-8")
        assert "Hello world" in content
        assert "# OCR Extracted Text" in content
        assert "# Page: 1" in content

    def test_creates_parent_directories(self, tmp_path, mock_tesseract):
        """Should create parent directories if needed."""
        out = tmp_path / "sub" / "dir" / "output.txt"
        save_text("test", out)
        assert out.exists()


class TestSaveAlto:
    """Tests for save_alto function."""

    def test_writes_bytes(self, tmp_path):
        """Should write ALTO XML bytes to file."""
        out = tmp_path / "output.xml"
        save_alto(SAMPLE_ALTO_XML, out)
        assert out.exists()
        assert out.read_bytes() == SAMPLE_ALTO_XML

    def test_creates_parent_directories(self, tmp_path):
        """Should create parent directories if needed."""
        out = tmp_path / "alto" / "sub" / "output.xml"
        save_alto(SAMPLE_ALTO_XML, out)
        assert out.exists()


# =============================================================================
# Clean Text NOT Applied to ALTO Tests
# =============================================================================


class TestAltoNotCleaned:
    """Verify that ALTO XML output is raw, not run through clean_ocr_text."""

    def test_alto_bytes_are_raw(self, mock_convert, mock_tesseract):
        """ALTO extraction should return raw bytes, not cleaned text."""
        result = extract_alto_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
        # The raw ALTO bytes should be identical to what pytesseract returned
        assert result[1] == SAMPLE_ALTO_XML

    def test_clean_ocr_text_not_called_for_alto(self, mock_convert, mock_tesseract):
        """clean_ocr_text should not be called on ALTO data."""
        with patch("ocr_processor.clean_ocr_text") as mock_clean:
            extract_alto_from_pdf(Path("dummy.pdf"), start_page=1, end_page=2)
            mock_clean.assert_not_called()


# =============================================================================
# ALTO Output Directory Tests
# =============================================================================


class TestAltoOutputDirectory:
    """Tests for ALTO output directory handling."""

    def test_save_alto_creates_directory(self, tmp_path):
        """save_alto should create the output directory."""
        alto_dir = tmp_path / "data" / "alto"
        out = alto_dir / "page_001.xml"
        save_alto(SAMPLE_ALTO_XML, out)
        assert alto_dir.exists()
        assert out.exists()

    def test_default_alto_dir_config(self):
        """ALTO_OUTPUT_DIR should point to data/alto/."""
        from ocr_processor import ALTO_OUTPUT_DIR
        assert ALTO_OUTPUT_DIR.name == "alto"
        assert "data" in str(ALTO_OUTPUT_DIR)


# =============================================================================
# Page Number Tests
# =============================================================================


class TestPageNumbering:
    """Tests for correct page numbering with offsets."""

    def test_text_extraction_page_offset(self, mock_convert, mock_tesseract):
        """Page numbers should start from start_page."""
        result = extract_text_from_pdf(Path("dummy.pdf"), start_page=5, end_page=6)
        assert 5 in result
        assert 6 in result
        assert 1 not in result

    def test_alto_extraction_page_offset(self, mock_convert, mock_tesseract):
        """ALTO page numbers should start from start_page."""
        result = extract_alto_from_pdf(Path("dummy.pdf"), start_page=5, end_page=6)
        assert 5 in result
        assert 6 in result


# =============================================================================
# Backward Compatibility Tests
# =============================================================================


class TestBackwardCompatibility:
    """Ensure default behavior is unchanged from original script."""

    def test_extract_text_signature_unchanged(self):
        """extract_text_from_pdf should accept same args as before."""
        import inspect
        sig = inspect.signature(extract_text_from_pdf)
        params = list(sig.parameters.keys())
        assert "pdf_path" in params
        assert "start_page" in params
        assert "end_page" in params

    def test_clean_ocr_text_unchanged(self):
        """clean_ocr_text should produce same output for same input."""
        text = "ſicut qvod VV ﬁrst"
        result = clean_ocr_text(text)
        assert "sicut" in result
        assert "quod" in result
        assert "W" in result
        assert "first" in result

    def test_identify_chapters_unchanged(self):
        """identify_chapters should work exactly as before."""
        text = "In DE PECCATO ORIGINIS we find DE IUSTIFICATIONE"
        chapters = identify_chapters(text)
        assert len(chapters) == 2


# =============================================================================
# Version Guard Tests
# =============================================================================


class TestVersionGuard:
    """Tests for the pytesseract version guard on image_to_alto_xml."""

    def test_alto_format_without_image_to_alto_xml(self):
        """Should exit with error when image_to_alto_xml is unavailable."""
        # Create a mock pytesseract that lacks image_to_alto_xml
        mock_pt = MagicMock(spec=["image_to_string", "get_tesseract_version"])
        mock_pt.get_tesseract_version.return_value = "4.0.0"

        with patch("ocr_processor.pytesseract", mock_pt), \
             patch("ocr_processor.PDF_PATH") as mock_pdf, \
             patch("sys.argv", ["ocr_processor", "--format", "alto"]):
            mock_pdf.exists.return_value = True

            with pytest.raises(SystemExit):
                main()

    def test_both_format_without_image_to_alto_xml(self):
        """Should also exit for --format both when image_to_alto_xml missing."""
        mock_pt = MagicMock(spec=["image_to_string", "get_tesseract_version"])
        mock_pt.get_tesseract_version.return_value = "4.0.0"

        with patch("ocr_processor.pytesseract", mock_pt), \
             patch("ocr_processor.PDF_PATH") as mock_pdf, \
             patch("sys.argv", ["ocr_processor", "--format", "both"]):
            mock_pdf.exists.return_value = True

            with pytest.raises(SystemExit):
                main()

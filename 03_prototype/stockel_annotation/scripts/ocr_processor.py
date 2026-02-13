#!/usr/bin/env python3
"""
OCR Processor for Stöckel's Annotationes in Locos communes (1561)

Extracts Latin text from scanned PDF pages using Tesseract OCR.
Outputs cleaned UTF-8 text files and/or ALTO XML for annotation in INCEpTION.

Usage:
    python ocr_processor.py [--pages START-END] [--output-dir DIR] [--single-file]
    python ocr_processor.py --format alto --pages 1-10
    python ocr_processor.py --format both --pages 1-10 --single-file
"""

import argparse
from datetime import datetime
import re
import sys
from pathlib import Path

try:
    from pdf2image import convert_from_path
    import pytesseract
except ImportError as e:
    # Allow tests to mock these modules before importing
    if "pytest" not in sys.modules:
        print(f"Missing dependency: {e}")
        print("Install with: pip install pdf2image pytesseract pillow")
        sys.exit(1)
    # Create stubs so the module can be imported in test environments
    convert_from_path = None  # type: ignore[assignment]
    pytesseract = None  # type: ignore[assignment]


# Configuration
PDF_PATH = Path(__file__).parent.parent / "data" / "raw" / "Annotationes Locorum Communium, 1561 - Stoeckel - first 58 pages.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "cleaned"
ALTO_OUTPUT_DIR = Path(__file__).parent.parent / "data" / "alto"
TESSERACT_LANG = "lat"  # Latin language pack
DPI = 300  # Higher DPI = better OCR but slower


# =============================================================================
# TEXT EXTRACTION
# =============================================================================


def extract_text_from_pdf(pdf_path: Path, start_page: int = 1, end_page: int | None = None) -> dict[int, str]:
    """
    Convert PDF pages to images and extract text using Tesseract OCR.

    Returns dict mapping page numbers to extracted text.
    """
    print(f"Loading PDF: {pdf_path.name}")

    # Convert PDF to images
    pages = convert_from_path(
        pdf_path,
        dpi=DPI,
        first_page=start_page,
        last_page=end_page
    )

    results = {}
    total_pages = len(pages)

    for i, page_image in enumerate(pages):
        page_num = start_page + i
        print(f"  Processing page {page_num}/{start_page + total_pages - 1}...", end=" ", flush=True)

        # Run Tesseract OCR with Latin language
        text = pytesseract.image_to_string(
            page_image,
            lang=TESSERACT_LANG,
            config='--psm 6'  # Assume uniform block of text
        )

        results[page_num] = text
        word_count = len(text.split())
        print(f"({word_count} words)")

    return results


# =============================================================================
# ALTO XML EXTRACTION
# =============================================================================


def extract_alto_from_pdf(pdf_path: Path, start_page: int = 1, end_page: int | None = None) -> dict[int, bytes]:
    """
    Convert PDF pages to images and extract ALTO XML using Tesseract OCR.

    Returns dict mapping page numbers to ALTO XML bytes.
    """
    print(f"Loading PDF: {pdf_path.name}")

    pages = convert_from_path(
        pdf_path,
        dpi=DPI,
        first_page=start_page,
        last_page=end_page
    )

    results = {}
    total_pages = len(pages)

    for i, page_image in enumerate(pages):
        page_num = start_page + i
        print(f"  Processing page {page_num}/{start_page + total_pages - 1} (ALTO)...", end=" ", flush=True)

        alto_xml = pytesseract.image_to_alto_xml(
            page_image,
            lang=TESSERACT_LANG,
            config='--psm 6'
        )

        results[page_num] = alto_xml
        print(f"({len(alto_xml):,} bytes)")

    return results


def extract_both_from_pdf(
    pdf_path: Path, start_page: int = 1, end_page: int | None = None
) -> tuple[dict[int, str], dict[int, bytes]]:
    """
    Convert PDF pages to images and extract both text and ALTO XML.

    Converts PDF to images once, then runs both pytesseract calls per page
    to avoid double PDF conversion.

    Returns tuple of (text_results, alto_results).
    """
    print(f"Loading PDF: {pdf_path.name}")

    pages = convert_from_path(
        pdf_path,
        dpi=DPI,
        first_page=start_page,
        last_page=end_page
    )

    text_results = {}
    alto_results = {}
    total_pages = len(pages)

    for i, page_image in enumerate(pages):
        page_num = start_page + i
        print(f"  Processing page {page_num}/{start_page + total_pages - 1}...", end=" ", flush=True)

        text = pytesseract.image_to_string(
            page_image,
            lang=TESSERACT_LANG,
            config='--psm 6'
        )
        alto_xml = pytesseract.image_to_alto_xml(
            page_image,
            lang=TESSERACT_LANG,
            config='--psm 6'
        )

        text_results[page_num] = text
        alto_results[page_num] = alto_xml
        word_count = len(text.split())
        print(f"({word_count} words, {len(alto_xml):,} bytes ALTO)")

    return text_results, alto_results


# =============================================================================
# TEXT CLEANING
# =============================================================================


def clean_ocr_text(text: str) -> str:
    """
    Clean and normalize OCR output for 16th-century Latin text.

    Handles common OCR errors and normalizes typography.
    """
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Fix common OCR errors in Latin
    replacements = [
        # Long s (ſ) often misread
        (r'ſ', 's'),
        # Ligatures
        (r'ﬁ', 'fi'),
        (r'ﬂ', 'fl'),
        (r'ﬀ', 'ff'),
        (r'ﬃ', 'ffi'),
        (r'ﬄ', 'ffl'),
        # Common misreads
        (r'\bvn\b', 'un'),  # v/u confusion in Latin
        (r'\bqvod\b', 'quod'),
        (r'VV', 'W'),
        (r'vv', 'w'),
        # Normalize quotation marks
        (r'[""„‟]', '"'),
        (r'[''‚‛]', "'"),
        # Remove excessive whitespace but preserve paragraph breaks
        (r'[ \t]+', ' '),
        (r'\n{3,}', '\n\n'),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    # Strip leading/trailing whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


# =============================================================================
# CHAPTER IDENTIFICATION
# =============================================================================


def identify_chapters(text: str) -> dict[str, tuple[int, int]]:
    """
    Attempt to identify chapter boundaries in the text.

    Returns dict mapping chapter names to (start_char, end_char) positions.
    """
    chapters = {}

    # Common chapter markers in theological Latin texts
    chapter_patterns = [
        r'DE PECCATO ORIG',
        r'DE IVSTIFICATIONE',
        r'DE IUSTIFICATIONE',
        r'DE LEGE ET EVANGELIO',
        r'DE LEGE & EVANGELIO',
    ]

    for pattern in chapter_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            chapters[pattern] = (match.start(), match.end())

    return chapters


# =============================================================================
# OUTPUT
# =============================================================================


def save_text(text: str, output_path: Path, metadata: dict | None = None):
    """Save extracted text with optional metadata header."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"""# OCR Extracted Text
# Source: Annotationes in Locos communes (1561) - Leonard Stöckel
# Extracted: {datetime.now().isoformat()}
# Language: Latin (lat)
# OCR Engine: Tesseract {pytesseract.get_tesseract_version()}
"""
    if metadata:
        for key, value in metadata.items():
            header += f"# {key}: {value}\n"

    header += "\n---\n\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header + text)

    print(f"Saved: {output_path}")


def save_alto(alto_xml: bytes, output_path: Path) -> None:
    """Save ALTO XML bytes to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(alto_xml)
    print(f"Saved: {output_path}")


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(description="OCR processor for Stöckel's Annotationes")
    parser.add_argument('--pages', type=str, default='1-58',
                        help='Page range to process (e.g., "1-10" or "5-20")')
    parser.add_argument('--output-dir', type=Path, default=OUTPUT_DIR,
                        help='Output directory for cleaned text')
    parser.add_argument('--alto-dir', type=Path, default=ALTO_OUTPUT_DIR,
                        help='Output directory for ALTO XML files')
    parser.add_argument('--single-file', action='store_true',
                        help='Output all pages to a single file')
    parser.add_argument('--format', choices=['txt', 'alto', 'both'], default='txt',
                        dest='output_format',
                        help='Output format: txt (default), alto, or both')
    args = parser.parse_args()

    # Parse page range
    try:
        if '-' in args.pages:
            start_str, end_str = args.pages.split('-', 1)
            start, end = int(start_str), int(end_str)
        else:
            start = end = int(args.pages)
    except ValueError:
        parser.error(
            f"Invalid page range '{args.pages}'. "
            "Use 'START-END' or a single integer page number (e.g., '1-10' or '5')."
        )

    if start > end:
        parser.error("Start page must be less than or equal to end page")

    # Ensure the source PDF exists before attempting OCR
    if not PDF_PATH.exists():
        parser.error(f"PDF file not found at {PDF_PATH}")

    # Check that image_to_alto_xml is available when needed
    if args.output_format in ('alto', 'both'):
        if pytesseract is None or not hasattr(pytesseract, 'image_to_alto_xml'):
            parser.error(
                "pytesseract.image_to_alto_xml() not available. "
                "Upgrade pytesseract: pip install --upgrade pytesseract>=0.3.8"
            )

    print(f"OCR Processing: Stöckel Annotationes")
    print(f"Pages: {start}-{end}")
    print(f"Format: {args.output_format}")
    if args.output_format in ('txt', 'both'):
        print(f"Text output: {args.output_dir}")
    if args.output_format in ('alto', 'both'):
        print(f"ALTO output: {args.alto_dir}")
    print("-" * 50)

    # -------------------------------------------------------------------------
    # Extract OCR data
    # -------------------------------------------------------------------------

    page_texts: dict[int, str] = {}
    page_altos: dict[int, bytes] = {}

    if args.output_format == 'txt':
        page_texts = extract_text_from_pdf(PDF_PATH, start, end)
    elif args.output_format == 'alto':
        page_altos = extract_alto_from_pdf(PDF_PATH, start, end)
    else:  # both
        page_texts, page_altos = extract_both_from_pdf(PDF_PATH, start, end)

    # -------------------------------------------------------------------------
    # Save plaintext output (txt or both)
    # -------------------------------------------------------------------------

    cleaned_texts: dict[int, str] = {}

    if page_texts:
        print("\nCleaning extracted text...")
        cleaned_texts = {page: clean_ocr_text(text) for page, text in page_texts.items()}

        if args.single_file:
            combined = "\n\n[PAGE BREAK]\n\n".join(
                f"[Page {page}]\n{text}"
                for page, text in sorted(cleaned_texts.items())
            )
            output_file = args.output_dir / f"annotationes_pp{start}-{end}.txt"
            save_text(combined, output_file, {"Pages": f"{start}-{end}"})
        else:
            for page, text in cleaned_texts.items():
                output_file = args.output_dir / f"annotationes_p{page:03d}.txt"
                save_text(text, output_file, {"Page": page})

    # -------------------------------------------------------------------------
    # Save ALTO XML output (alto or both)
    # -------------------------------------------------------------------------

    if page_altos:
        print("\nSaving ALTO XML files...")
        if args.single_file:
            print("  Note: --single-file not applicable for ALTO XML; saving per-page files.")
            print("  Use extract_alto.py batch mode to process all files at once.")

        for page, alto_xml in page_altos.items():
            output_file = args.alto_dir / f"annotationes_p{page:03d}.xml"
            save_alto(alto_xml, output_file)

    # -------------------------------------------------------------------------
    # Chapter analysis (only when plaintext is available)
    # -------------------------------------------------------------------------

    if cleaned_texts:
        print("\nSearching for chapter markers...")
        all_text = " ".join(cleaned_texts.values())
        chapters = identify_chapters(all_text)
        if chapters:
            print("Found potential chapter markers:")
            for name, (start_pos, end_pos) in chapters.items():
                print(f"  - {name} (position {start_pos}-{end_pos})")
        else:
            print("  No chapter markers detected (may need manual identification)")

    # -------------------------------------------------------------------------
    # Summary statistics
    # -------------------------------------------------------------------------

    print(f"\nSummary:")
    num_pages = max(len(page_texts), len(page_altos))
    print(f"  Pages processed: {num_pages}")

    if cleaned_texts:
        total_words = sum(len(text.split()) for text in cleaned_texts.values())
        total_chars = sum(len(text) for text in cleaned_texts.values())
        print(f"  Total words: {total_words:,}")
        print(f"  Total characters: {total_chars:,}")
        print(f"  Text output: {args.output_dir}")

    if page_altos:
        total_alto_size = sum(len(xml) for xml in page_altos.values())
        print(f"  ALTO XML files: {len(page_altos)}")
        print(f"  Total ALTO size: {total_alto_size:,} bytes")
        print(f"  ALTO output: {args.alto_dir}")
        print(f"\n  Next step: python extract_alto.py {args.alto_dir}/ -o {args.output_dir}/ --export-confidence")


if __name__ == "__main__":
    main()

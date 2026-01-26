#!/usr/bin/env python3
"""
OCR Processor for Stöckel's Annotationes in Locos communes (1561)

Extracts Latin text from scanned PDF pages using Tesseract OCR.
Outputs cleaned UTF-8 text files for annotation in INCEpTION.

Usage:
    python ocr_processor.py [--pages START-END] [--output-dir DIR]
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install pdf2image pytesseract pillow")
    sys.exit(1)


# Configuration
PDF_PATH = Path(__file__).parent.parent / "data" / "raw" / "Annotationes Locorum Communium, 1561 - Stoeckel - first 58 pages.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "cleaned"
TESSERACT_LANG = "lat"  # Latin language pack
DPI = 300  # Higher DPI = better OCR but slower


def extract_text_from_pdf(pdf_path: Path, start_page: int = 1, end_page: int = None) -> dict[int, str]:
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
            chapters[pattern] = match.start()

    return chapters


def save_text(text: str, output_path: Path, metadata: dict = None):
    """Save extracted text with optional metadata header."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"""# OCR Extracted Text
# Source: Annotationes in Locos communes (1561) - Leonard Stöckel
# Extracted: {__import__('datetime').datetime.now().isoformat()}
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


def main():
    parser = argparse.ArgumentParser(description="OCR processor for Stöckel's Annotationes")
    parser.add_argument('--pages', type=str, default='1-58',
                        help='Page range to process (e.g., "1-10" or "5-20")')
    parser.add_argument('--output-dir', type=Path, default=OUTPUT_DIR,
                        help='Output directory for cleaned text')
    parser.add_argument('--single-file', action='store_true',
                        help='Output all pages to a single file')
    args = parser.parse_args()

    # Parse page range
    if '-' in args.pages:
        start, end = map(int, args.pages.split('-'))
    else:
        start = end = int(args.pages)

    print(f"OCR Processing: Stöckel Annotationes")
    print(f"Pages: {start}-{end}")
    print(f"Output: {args.output_dir}")
    print("-" * 50)

    # Extract text
    page_texts = extract_text_from_pdf(PDF_PATH, start, end)

    # Clean all texts
    print("\nCleaning extracted text...")
    cleaned_texts = {page: clean_ocr_text(text) for page, text in page_texts.items()}

    # Save output
    if args.single_file:
        # Combine all pages into one file
        combined = "\n\n[PAGE BREAK]\n\n".join(
            f"[Page {page}]\n{text}"
            for page, text in sorted(cleaned_texts.items())
        )
        output_file = args.output_dir / f"annotationes_pp{start}-{end}.txt"
        save_text(combined, output_file, {"Pages": f"{start}-{end}"})
    else:
        # Save each page separately
        for page, text in cleaned_texts.items():
            output_file = args.output_dir / f"annotationes_p{page:03d}.txt"
            save_text(text, output_file, {"Page": page})

    # Analyze for chapter markers
    print("\nSearching for chapter markers...")
    all_text = " ".join(cleaned_texts.values())
    chapters = identify_chapters(all_text)
    if chapters:
        print("Found potential chapter markers:")
        for name, pos in chapters.items():
            print(f"  - {name} (position ~{pos})")
    else:
        print("  No chapter markers detected (may need manual identification)")

    # Summary statistics
    total_words = sum(len(text.split()) for text in cleaned_texts.values())
    total_chars = sum(len(text) for text in cleaned_texts.values())
    print(f"\nSummary:")
    print(f"  Pages processed: {len(cleaned_texts)}")
    print(f"  Total words: {total_words:,}")
    print(f"  Total characters: {total_chars:,}")
    print(f"  Output location: {args.output_dir}")


if __name__ == "__main__":
    main()

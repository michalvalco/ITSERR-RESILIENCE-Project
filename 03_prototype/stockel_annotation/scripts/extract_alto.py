#!/usr/bin/env python3
"""
ALTO XML → Plaintext Extraction for Stöckel's Annotationes (1561)

Parses ALTO XML files (v2.x and v3.x) produced by Tesseract OCR and extracts
clean plaintext preserving reading order, page/paragraph/line structure, and
handling hyphenation. Optionally exports per-word OCR confidence scores as CSV.

Output is formatted with [Page N] and [PAGE BREAK] markers compatible with
the downstream normalize_text.py pipeline.

Usage:
    # Single file
    python extract_alto.py input.xml -o output.txt

    # With confidence CSV and minimum confidence filter
    python extract_alto.py input.xml -o output.txt --confidence scores.csv --min-confidence 0.5

    # Page range
    python extract_alto.py input.xml -o output.txt --pages 1-10

    # Batch mode (directory of ALTO XMLs)
    python extract_alto.py input_dir/ -o output_dir/ --recursive

Python API:
    from extract_alto import extract_text_from_alto
    text = extract_text_from_alto("input.xml")
"""

import argparse
import csv
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("Missing dependency: lxml")
    print("Install with: pip install lxml")
    sys.exit(1)


# Configure logging
logger = logging.getLogger(__name__)

# Known ALTO namespace URIs
ALTO_NAMESPACES = [
    "http://www.loc.gov/standards/alto/ns-v3#",
    "http://www.loc.gov/standards/alto/ns-v2#",
    "http://schema.ccs-gmbh.com/ALTO",
]


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class WordInfo:
    """OCR confidence and location data for a single word."""
    content: str
    confidence: float | None
    page: int
    line_id: str
    subs_type: str | None = None
    subs_content: str | None = None


@dataclass
class ExtractionStats:
    """Track extraction statistics for reporting."""
    total_pages: int = 0
    total_words: int = 0
    total_confidence_sum: float = 0.0
    words_with_confidence: int = 0
    words_below_threshold: int = 0
    pages_needing_review: list[int] = field(default_factory=list)
    skipped_elements: int = 0


# =============================================================================
# ALTO XML PARSING
# =============================================================================


def detect_namespace(tree: etree._ElementTree) -> str | None:
    """
    Detect the ALTO namespace used in the document.

    Returns the namespace URI string, or None if no namespace is used.
    """
    root = tree.getroot()
    root_tag = root.tag

    # Check if root uses a namespace (Clark notation: {uri}localname)
    if root_tag.startswith("{"):
        ns = root_tag.split("}")[0][1:]
        if ns in ALTO_NAMESPACES:
            return ns
        # Unknown namespace — still usable
        logger.debug("Non-standard ALTO namespace: %s", ns)
        return ns

    # No namespace on root — check if children use one
    for child in root.iter():
        if child.tag.startswith("{"):
            ns = child.tag.split("}")[0][1:]
            return ns

    return None


def _xpath(element: etree._Element, local_name: str, ns: str | None) -> list:
    """Find child elements by local name, handling namespace variations."""
    if ns:
        return element.findall(f"{{{ns}}}{local_name}")
    return element.findall(local_name)


def _xpath_descendants(element: etree._Element, local_name: str, ns: str | None) -> list:
    """Find descendant elements by local name, handling namespace variations."""
    if ns:
        return element.findall(f".//{{{ns}}}{local_name}")
    return element.findall(f".//{local_name}")


def parse_alto_file(
    file_path: Path,
    page_range: tuple[int, int] | None = None,
) -> tuple[list[list[list[list[WordInfo]]]], str | None]:
    """
    Parse an ALTO XML file into a structured representation.

    Returns:
        Tuple of (pages, namespace) where pages is a nested list:
        pages[page_idx][block_idx][line_idx] = list of WordInfo
    """
    tree = _parse_xml(file_path)
    ns = detect_namespace(tree)
    root = tree.getroot()

    pages_data: list[list[list[list[WordInfo]]]] = []

    # Find all Page elements
    page_elements = _xpath_descendants(root, "Page", ns)
    if not page_elements:
        logger.warning("No <Page> elements found in %s", file_path)
        return [], ns

    for page_idx, page_el in enumerate(page_elements):
        page_num = page_idx + 1

        # Apply page range filter
        if page_range:
            start, end = page_range
            if page_num < start:
                continue
            if page_num > end:
                break

        blocks_data: list[list[list[WordInfo]]] = []

        # Find PrintSpace or fall back to the Page element itself
        print_spaces = _xpath(page_el, "PrintSpace", ns)
        containers = print_spaces if print_spaces else [page_el]

        for container in containers:
            text_blocks = _xpath_descendants(container, "TextBlock", ns)
            if not text_blocks:
                # Try ComposedBlock → TextBlock nesting
                composed = _xpath_descendants(container, "ComposedBlock", ns)
                for cb in composed:
                    text_blocks.extend(_xpath(cb, "TextBlock", ns))

            for block_el in text_blocks:
                lines_data: list[list[WordInfo]] = []

                text_lines = _xpath(block_el, "TextLine", ns)
                for line_el in text_lines:
                    line_id = line_el.get("ID", "")
                    words_data: list[WordInfo] = []

                    for child in line_el:
                        local = etree.QName(child).localname if isinstance(child.tag, str) else None
                        if local == "String":
                            word = _parse_string_element(child, page_num, line_id)
                            if word:
                                words_data.append(word)
                        # SP and HYP elements are handled implicitly

                    if words_data:
                        lines_data.append(words_data)

                if lines_data:
                    blocks_data.append(lines_data)

        pages_data.append(blocks_data)

    return pages_data, ns


def _parse_xml(file_path: Path) -> etree._ElementTree:
    """
    Parse an XML file with encoding fallback.

    Tries UTF-8 first, falls back to Latin-1 on encoding errors.
    """
    try:
        return etree.parse(str(file_path))
    except etree.XMLSyntaxError:
        # Try with explicit Latin-1 encoding
        logger.debug("UTF-8 parse failed for %s, trying Latin-1", file_path)
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()
        return etree.fromstring(content.encode("utf-8")).getroottree()


def _parse_string_element(el: etree._Element, page_num: int, line_id: str) -> WordInfo | None:
    """Parse a <String> element into a WordInfo."""
    content = el.get("CONTENT")
    if content is None:
        logger.debug("String element missing CONTENT attribute on page %d", page_num)
        return None

    # Parse confidence (WC attribute, 0.0–1.0)
    wc_raw = el.get("WC")
    confidence: float | None = None
    if wc_raw is not None:
        try:
            confidence = float(wc_raw)
        except ValueError:
            logger.debug("Invalid WC value '%s' on page %d", wc_raw, page_num)

    return WordInfo(
        content=content,
        confidence=confidence,
        page=page_num,
        line_id=line_id,
        subs_type=el.get("SUBS_TYPE"),
        subs_content=el.get("SUBS_CONTENT"),
    )


# =============================================================================
# TEXT ASSEMBLY
# =============================================================================


def assemble_text(
    pages: list[list[list[list[WordInfo]]]],
    page_offset: int = 0,
) -> str:
    """
    Assemble plaintext from parsed ALTO structure.

    Handles hyphenation rejoining using SUBS_TYPE/SUBS_CONTENT attributes.
    Output uses [Page N] and [PAGE BREAK] markers for normalize_text.py compatibility.
    """
    if not pages:
        return ""

    output_parts: list[str] = []

    for page_idx, blocks in enumerate(pages):
        page_num = page_offset + page_idx + 1

        if page_idx > 0:
            output_parts.append("\n[PAGE BREAK]\n")
        output_parts.append(f"[Page {page_num}]\n")

        for block_idx, lines in enumerate(blocks):
            if block_idx > 0:
                output_parts.append("")  # Blank line between TextBlocks

            for line in lines:
                line_text = _assemble_line(line)
                output_parts.append(line_text)

    return "\n".join(output_parts)


def _assemble_line(words: list[WordInfo]) -> str:
    """
    Assemble a single TextLine's words into a string.

    Handles hyphenation: when a word has SUBS_TYPE="HypPart1", use
    SUBS_CONTENT for the full word and skip the corresponding HypPart2.
    """
    parts: list[str] = []
    skip_next_hyp2 = False

    for word in words:
        if skip_next_hyp2 and word.subs_type == "HypPart2":
            skip_next_hyp2 = False
            continue

        if word.subs_type == "HypPart1":
            # Use the substitution content (full rejoined word) if available
            if word.subs_content:
                parts.append(word.subs_content)
            else:
                # Fallback: just use the content as-is (will include trailing hyphen)
                parts.append(word.content)
            skip_next_hyp2 = True
        elif word.subs_type == "HypPart2":
            # If we reach HypPart2 without a preceding HypPart1 (shouldn't happen
            # in well-formed ALTO, but handle gracefully), just skip it since the
            # full word was already emitted from HypPart1
            continue
        else:
            parts.append(word.content)

    return " ".join(parts)


# =============================================================================
# CONFIDENCE EXTRACTION
# =============================================================================


def collect_word_confidence(
    pages: list[list[list[list[WordInfo]]]],
    page_offset: int = 0,
) -> list[dict[str, str | float | int]]:
    """
    Collect per-word confidence data for CSV export.

    Returns list of dicts with keys: word, confidence, page, line.
    """
    rows: list[dict[str, str | float | int]] = []

    for page_idx, blocks in enumerate(pages):
        page_num = page_offset + page_idx + 1
        for lines in blocks:
            for words in lines:
                for word in words:
                    rows.append({
                        "word": word.content,
                        "confidence": word.confidence if word.confidence is not None else "",
                        "page": page_num,
                        "line": word.line_id,
                    })

    return rows


def write_confidence_csv(rows: list[dict], output_path: Path) -> None:
    """Write confidence data to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["word", "confidence", "page", "line"])
        writer.writeheader()
        writer.writerows(rows)

    logger.info("Confidence CSV written to %s", output_path)


# =============================================================================
# STATISTICS
# =============================================================================


def compute_stats(
    pages: list[list[list[list[WordInfo]]]],
    confidence_threshold: float = 0.7,
    page_offset: int = 0,
) -> ExtractionStats:
    """Compute extraction statistics from parsed ALTO data."""
    stats = ExtractionStats()
    stats.total_pages = len(pages)

    for page_idx, blocks in enumerate(pages):
        page_num = page_offset + page_idx + 1
        page_conf_sum = 0.0
        page_conf_count = 0

        for lines in blocks:
            for words in lines:
                for word in words:
                    stats.total_words += 1
                    if word.confidence is not None:
                        stats.total_confidence_sum += word.confidence
                        stats.words_with_confidence += 1
                        page_conf_sum += word.confidence
                        page_conf_count += 1
                        if word.confidence < confidence_threshold:
                            stats.words_below_threshold += 1

        # Flag pages with low mean confidence
        if page_conf_count > 0:
            page_mean = page_conf_sum / page_conf_count
            if page_mean < confidence_threshold:
                stats.pages_needing_review.append(page_num)

    return stats


def log_stats(stats: ExtractionStats, confidence_threshold: float = 0.7) -> None:
    """Log extraction summary statistics."""
    mean_conf = (
        stats.total_confidence_sum / stats.words_with_confidence
        if stats.words_with_confidence > 0
        else 0.0
    )

    logger.info("Extraction summary:")
    logger.info("  Total pages:       %d", stats.total_pages)
    logger.info("  Total words:       %d", stats.total_words)
    logger.info("  Mean confidence:   %.3f", mean_conf)
    logger.info(
        "  Words below %.1f:   %d", confidence_threshold, stats.words_below_threshold
    )

    if stats.pages_needing_review:
        logger.warning(
            "  Pages needing review (mean conf < %.1f): %s",
            confidence_threshold,
            ", ".join(str(p) for p in stats.pages_needing_review),
        )


# =============================================================================
# PUBLIC API
# =============================================================================


def extract_text_from_alto(
    alto_path: str | Path,
    page_range: tuple[int, int] | None = None,
    confidence_threshold: float = 0.7,
) -> str:
    """
    Extract plaintext from an ALTO XML file.

    Args:
        alto_path: Path to the ALTO XML file.
        page_range: Optional (start, end) inclusive page range to extract.
        confidence_threshold: Confidence threshold for quality warnings.

    Returns:
        Extracted plaintext with page markers.
    """
    alto_path = Path(alto_path)
    pages, _ = parse_alto_file(alto_path, page_range=page_range)
    page_offset = (page_range[0] - 1) if page_range else 0

    stats = compute_stats(pages, confidence_threshold, page_offset=page_offset)
    log_stats(stats, confidence_threshold)

    return assemble_text(pages, page_offset=page_offset)


def extract_confidence_from_alto(
    alto_path: str | Path,
    page_range: tuple[int, int] | None = None,
) -> list[dict[str, str | float | int]]:
    """
    Extract per-word confidence data from an ALTO XML file.

    Args:
        alto_path: Path to the ALTO XML file.
        page_range: Optional (start, end) inclusive page range to extract.

    Returns:
        List of dicts with keys: word, confidence, page, line.
    """
    alto_path = Path(alto_path)
    pages, _ = parse_alto_file(alto_path, page_range=page_range)
    page_offset = (page_range[0] - 1) if page_range else 0
    return collect_word_confidence(pages, page_offset=page_offset)


# =============================================================================
# BATCH PROCESSING
# =============================================================================


def process_batch(
    input_dir: Path,
    output_dir: Path,
    recursive: bool = False,
    confidence_csv: bool = False,
    page_range: tuple[int, int] | None = None,
    confidence_threshold: float = 0.7,
) -> None:
    """
    Process a directory of ALTO XML files.

    Finds all .xml files in input_dir and writes corresponding .txt files
    to output_dir, preserving subdirectory structure if recursive.
    """
    pattern = "**/*.xml" if recursive else "*.xml"
    xml_files = sorted(input_dir.glob(pattern))

    if not xml_files:
        logger.warning("No XML files found in %s", input_dir)
        return

    logger.info("Found %d XML files to process", len(xml_files))
    output_dir.mkdir(parents=True, exist_ok=True)

    for xml_file in xml_files:
        relative = xml_file.relative_to(input_dir)
        out_txt = output_dir / relative.with_suffix(".txt")
        out_txt.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Processing: %s", xml_file.name)
        try:
            text = extract_text_from_alto(
                xml_file, page_range=page_range, confidence_threshold=confidence_threshold,
            )
            out_txt.write_text(text, encoding="utf-8")
            logger.info("  → %s", out_txt.name)

            if confidence_csv:
                out_csv = out_txt.with_suffix(".confidence.csv")
                rows = extract_confidence_from_alto(xml_file, page_range=page_range)
                write_confidence_csv(rows, out_csv)
        except etree.XMLSyntaxError as e:
            logger.error("Malformed XML in %s: %s", xml_file.name, e)
        except Exception as e:
            logger.error("Failed to process %s: %s", xml_file.name, e)


# =============================================================================
# CLI
# =============================================================================


def parse_page_range(value: str) -> tuple[int, int]:
    """Parse a page range string like '1-10' or '5' into a (start, end) tuple."""
    if "-" in value:
        start_str, end_str = value.split("-", 1)
        start, end = int(start_str), int(end_str)
    else:
        start = end = int(value)

    if start < 1:
        raise ValueError("Start page must be >= 1")
    if start > end:
        raise ValueError("Start page must be <= end page")

    return start, end


def main():
    parser = argparse.ArgumentParser(
        description="Extract plaintext from ALTO XML files (Stöckel annotation pipeline)"
    )
    parser.add_argument(
        "input", type=Path,
        help="Input ALTO XML file or directory (batch mode)"
    )
    parser.add_argument(
        "-o", "--output", type=Path, required=True,
        help="Output text file or directory (batch mode)"
    )
    parser.add_argument(
        "--confidence", type=Path, default=None,
        help="Output confidence CSV file (single-file mode)"
    )
    parser.add_argument(
        "--min-confidence", type=float, default=0.7,
        help="Confidence threshold for quality warnings (default: 0.7)"
    )
    parser.add_argument(
        "--pages", type=str, default=None,
        help='Page range to extract (e.g., "1-10" or "5")'
    )
    parser.add_argument(
        "--recursive", action="store_true",
        help="Recursively search for XML files in batch mode"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose (DEBUG) logging"
    )
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    # Parse page range
    page_range = None
    if args.pages:
        try:
            page_range = parse_page_range(args.pages)
        except ValueError as e:
            parser.error(f"Invalid page range '{args.pages}': {e}")

    # Batch vs single-file mode
    if args.input.is_dir():
        process_batch(
            input_dir=args.input,
            output_dir=args.output,
            recursive=args.recursive,
            confidence_csv=args.confidence is not None,
            page_range=page_range,
            confidence_threshold=args.min_confidence,
        )
    elif args.input.is_file():
        try:
            text = extract_text_from_alto(
                args.input,
                page_range=page_range,
                confidence_threshold=args.min_confidence,
            )
        except etree.XMLSyntaxError as e:
            logger.error("Malformed XML: %s", e)
            sys.exit(1)

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        logger.info("Output written to %s", args.output)

        if args.confidence:
            rows = extract_confidence_from_alto(args.input, page_range=page_range)
            write_confidence_csv(rows, args.confidence)
    else:
        parser.error(f"Input path does not exist: {args.input}")


if __name__ == "__main__":
    main()

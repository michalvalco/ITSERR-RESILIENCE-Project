#!/usr/bin/env python3
"""
CAS XMI → BIOES Converter for INCEpTION Annotation Exports

Converts INCEpTION CAS XMI annotation exports to BIOES-tagged token sequences
for CRF model training. Adapted from the GNORM CIC_annotation pipeline
(https://github.com/aesuli/CIC_annotation) for the Stöckel theological
annotation project.

BIOES labelling scheme:
    B - Beginning of a multi-token entity
    I - Inside a multi-token entity
    E - End of a multi-token entity
    S - Single-token entity
    O - Outside any entity

Input: ZIP file exported from INCEpTION containing:
    - TypeSystem.xml   — UIMA type system definitions
    - <annotator>/*.xmi — annotated documents in CAS XMI format

Output: One .bioes file per document, each containing:
    token  start_offset  end_offset  label

Usage:
    python cas_to_bioes.py <zip_file> <annotator_username> [--output-dir DIR]
    python cas_to_bioes.py --from-xmi <xmi_file> --typesystem <ts_file> [--output-dir DIR]

Dependencies:
    dkpro-cassis >= 0.9.0  (listed in pyproject.toml [annotation] extras)
"""

import argparse
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from cassis import Cas, load_cas_from_xmi, load_typesystem
    HAS_CASSIS = True
except ImportError:
    HAS_CASSIS = False
    Cas = None  # type: ignore[assignment,misc]


# Default annotation layer names (INCEpTION / WebAnno conventions)
# GNORM uses webanno.custom.Glossa; Stöckel project may use custom layers
DEFAULT_ANNOTATION_TYPES = [
    "webanno.custom.Glossa",                    # GNORM legal references
    "webanno.custom.BiblicalReference",         # Stöckel biblical refs
    "webanno.custom.PatristicReference",        # Stöckel patristic refs
    "webanno.custom.ReformationReference",      # Stöckel reformation refs
    "de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity",  # Standard NER
]

TOKEN_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
SENTENCE_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"

# Default output directory
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "data" / "bioes"


@dataclass
class ConversionStats:
    """Track conversion statistics for reporting."""
    documents_processed: int = 0
    total_tokens: int = 0
    total_annotations: int = 0
    total_sentences: int = 0
    annotations_by_type: dict = field(default_factory=dict)
    documents_skipped: int = 0


def get_annotation_type_label(annotation, type_feature: Optional[str] = None) -> str:
    """
    Extract a label string from an annotation.

    Tries multiple strategies:
    1. If type_feature is specified, use that feature's value
    2. Try common feature names: 'Tipo', 'value', 'label', 'NamedEntityType'
    3. Fall back to the short type name (e.g., 'Glossa' → 'AN')
    """
    # Strategy 1: explicit feature name
    if type_feature:
        try:
            val = annotation.get(type_feature)
            if val:
                return _normalize_label(str(val))
        except Exception:
            pass

    # Strategy 2: try common feature names
    for feat in ("Tipo", "value", "label", "NamedEntityType", "category"):
        try:
            val = annotation.get(feat)
            if val:
                return _normalize_label(str(val))
        except Exception:
            continue

    # Strategy 3: derive from annotation type name
    type_name = type(annotation).__name__
    return _type_name_to_label(type_name)


def _normalize_label(raw: str) -> str:
    """Normalize an annotation value to a short label."""
    label_map = {
        # GNORM labels
        "Allegazione normativa": "AN",
        "Lemma glossato": "LEMMA",
        "Capitolo": "CHAPTER",
        "Titolo": "TITLE",
        # Stöckel labels
        "Biblical reference": "BIB",
        "Biblical_Reference": "BIB",
        "BiblicalReference": "BIB",
        "Patristic reference": "PAT",
        "Patristic_Reference": "PAT",
        "PatristicReference": "PAT",
        "Reformation reference": "REF",
        "Reformation_Reference": "REF",
        "ReformationReference": "REF",
    }
    # Strip multi-span group suffixes like [1], [2]
    cleaned = raw.split("[")[0].strip()
    return label_map.get(cleaned, cleaned.upper().replace(" ", "_"))


def _type_name_to_label(type_name: str) -> str:
    """Convert a UIMA type name to a short label."""
    short_name_map = {
        "Glossa": "AN",
        "BiblicalReference": "BIB",
        "PatristicReference": "PAT",
        "ReformationReference": "REF",
        "NamedEntity": "NE",
    }
    # Get the last segment of the fully-qualified name
    short = type_name.rsplit(".", 1)[-1]
    return short_name_map.get(short, short.upper())


def tokenize_text(text: str) -> list[tuple[str, int, int]]:
    """
    Simple whitespace + punctuation tokenizer with character offsets.

    Used as a fallback when no Token annotations are present in the CAS.
    Returns list of (token_text, start_offset, end_offset) tuples.
    """
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        # Skip whitespace
        while i < n and text[i].isspace():
            i += 1
        if i >= n:
            break

        start = i
        char = text[i]

        # Single-character punctuation tokens
        if char in ".,;:!?()[]{}«»–—\"'§†‡":
            tokens.append((char, start, start + 1))
            i += 1
        else:
            # Alphanumeric or other runs
            while i < n and not text[i].isspace() and text[i] not in ".,;:!?()[]{}«»–—\"'§†‡":
                i += 1
            tokens.append((text[start:i], start, i))

    return tokens


def get_tokens_from_cas(cas: Cas) -> list[tuple[str, int, int]]:
    """
    Extract tokens from the CAS, falling back to simple tokenization.

    Returns list of (token_text, start_offset, end_offset) tuples,
    sorted by start offset.
    """
    tokens = []
    try:
        for token in cas.select(TOKEN_TYPE):
            tok_text = cas.get_covered_text(token)
            if tok_text and tok_text.strip():
                tokens.append((tok_text, token.begin, token.end))
    except Exception:
        pass  # Type not in typesystem

    if tokens:
        tokens.sort(key=lambda t: t[1])
        return tokens

    # Fallback: tokenize the sofa string
    sofa_text = cas.sofa_string
    if sofa_text:
        return tokenize_text(sofa_text)

    return []


def get_sentences_from_cas(cas: Cas) -> list[tuple[int, int]]:
    """
    Extract sentence boundaries from the CAS.

    Returns list of (start_offset, end_offset) tuples, sorted by start offset.
    Falls back to treating the whole document as one sentence.
    """
    sentences = []
    try:
        for sent in cas.select(SENTENCE_TYPE):
            sentences.append((sent.begin, sent.end))
    except Exception:
        pass

    if sentences:
        sentences.sort(key=lambda s: s[0])
        return sentences

    # Fallback: entire document is one sentence
    sofa_text = cas.sofa_string or ""
    if sofa_text:
        return [(0, len(sofa_text))]
    return []


def get_annotations_from_cas(
    cas: Cas,
    annotation_types: list[str],
    type_feature: Optional[str] = None,
) -> list[tuple[int, int, str]]:
    """
    Extract entity annotations from the CAS.

    Returns list of (start_offset, end_offset, label) tuples,
    sorted by start offset (then end offset for ties).
    """
    annotations = []
    for ann_type in annotation_types:
        try:
            for ann in cas.select(ann_type):
                label = get_annotation_type_label(ann, type_feature)
                annotations.append((ann.begin, ann.end, label))
        except Exception:
            continue  # Type not in this typesystem

    annotations.sort(key=lambda a: (a[0], a[1]))
    return annotations


def assign_bioes_labels(
    tokens: list[tuple[str, int, int]],
    annotations: list[tuple[int, int, str]],
) -> list[str]:
    """
    Assign BIOES labels to tokens based on annotation spans.

    For each annotation span, tokens overlapping with it are assigned
    B/I/E/S labels depending on their position within the span.
    Tokens not covered by any annotation get label 'O'.
    """
    labels = ["O"] * len(tokens)

    for ann_start, ann_end, ann_label in annotations:
        # Find all tokens overlapping with this annotation span
        span_indices = []
        for idx, (_, tok_start, tok_end) in enumerate(tokens):
            # Token overlaps annotation if they share any characters
            if tok_start < ann_end and tok_end > ann_start:
                span_indices.append(idx)

        if not span_indices:
            continue

        if len(span_indices) == 1:
            labels[span_indices[0]] = f"S-{ann_label}"
        else:
            labels[span_indices[0]] = f"B-{ann_label}"
            for mid_idx in span_indices[1:-1]:
                labels[mid_idx] = f"I-{ann_label}"
            labels[span_indices[-1]] = f"E-{ann_label}"

    return labels


def tokens_in_sentence(
    tokens: list[tuple[str, int, int]],
    sent_start: int,
    sent_end: int,
) -> list[int]:
    """Return indices of tokens that fall within a sentence boundary."""
    indices = []
    for idx, (_, tok_start, tok_end) in enumerate(tokens):
        # Token belongs to sentence if its midpoint is within the sentence
        tok_mid = (tok_start + tok_end) / 2
        if sent_start <= tok_mid < sent_end:
            indices.append(idx)
    return indices


def convert_cas_to_bioes(
    cas: Cas,
    annotation_types: list[str],
    type_feature: Optional[str] = None,
) -> tuple[list[list[tuple[str, int, int, str]]], ConversionStats]:
    """
    Convert a single CAS document to BIOES-labelled sentences.

    Returns:
        sentences: list of sentences, each a list of (token, start, end, label) tuples
        stats: conversion statistics for this document
    """
    stats = ConversionStats()

    tokens = get_tokens_from_cas(cas)
    if not tokens:
        return [], stats

    annotations = get_annotations_from_cas(cas, annotation_types, type_feature)
    labels = assign_bioes_labels(tokens, annotations)
    sentences_bounds = get_sentences_from_cas(cas)

    stats.total_tokens = len(tokens)
    stats.total_annotations = len(annotations)
    stats.total_sentences = len(sentences_bounds)

    # Count annotations by type
    for _, _, label in annotations:
        stats.annotations_by_type[label] = stats.annotations_by_type.get(label, 0) + 1

    # Group tokens into sentences
    result_sentences = []
    for sent_start, sent_end in sentences_bounds:
        sent_indices = tokens_in_sentence(tokens, sent_start, sent_end)
        if sent_indices:
            sent_data = [
                (tokens[i][0], tokens[i][1], tokens[i][2], labels[i])
                for i in sent_indices
            ]
            result_sentences.append(sent_data)

    return result_sentences, stats


def format_bioes_output(sentences: list[list[tuple[str, int, int, str]]]) -> str:
    """
    Format BIOES-labelled sentences as a string.

    Output format (one token per line, blank line between sentences):
        token start_offset end_offset label
    """
    lines = []
    for sent_idx, sentence in enumerate(sentences):
        if sent_idx > 0:
            lines.append("")  # blank line separates sentences
        for token, start, end, label in sentence:
            lines.append(f"{token} {start} {end} {label}")
    return "\n".join(lines) + "\n" if lines else ""


def _require_cassis() -> None:
    """Raise an error if dkpro-cassis is not installed."""
    if not HAS_CASSIS:
        print(
            "ERROR: dkpro-cassis is required but not installed.\n"
            "Install with: pip install 'itserr-agent[annotation]'",
            file=sys.stderr,
        )
        sys.exit(1)


def process_zip(
    zip_path: Path,
    annotator: str,
    output_dir: Path,
    annotation_types: list[str],
    type_feature: Optional[str] = None,
) -> ConversionStats:
    """
    Process an INCEpTION ZIP export.

    The ZIP structure expected:
        <zip>/TypeSystem.xml
        <zip>/<annotator>/<document>.xmi
    """
    _require_cassis()
    total_stats = ConversionStats()
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Find TypeSystem.xml
        ts_candidates = [n for n in zf.namelist() if n.endswith("TypeSystem.xml")]
        if not ts_candidates:
            print("ERROR: No TypeSystem.xml found in ZIP", file=sys.stderr)
            sys.exit(1)

        # Load typesystem
        with zf.open(ts_candidates[0]) as ts_file:
            typesystem = load_typesystem(ts_file)

        # Find annotator XMI files
        annotator_prefix = f"{annotator}/"
        xmi_files = [
            n for n in zf.namelist()
            if n.startswith(annotator_prefix) and n.endswith(".xmi")
        ]

        if not xmi_files:
            # Try without annotator prefix (flat structure)
            xmi_files = [n for n in zf.namelist() if n.endswith(".xmi")]

        if not xmi_files:
            print(f"ERROR: No XMI files found for annotator '{annotator}'", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(xmi_files)} XMI files for annotator '{annotator}'")

        for xmi_name in sorted(xmi_files):
            doc_name = Path(xmi_name).stem
            print(f"  Processing: {doc_name}")

            with zf.open(xmi_name) as xmi_file:
                try:
                    cas = load_cas_from_xmi(xmi_file, typesystem=typesystem)
                except Exception as e:
                    print(f"    WARNING: Failed to load {xmi_name}: {e}", file=sys.stderr)
                    total_stats.documents_skipped += 1
                    continue

            sentences, doc_stats = convert_cas_to_bioes(
                cas, annotation_types, type_feature
            )

            if not sentences:
                print(f"    WARNING: No tokens found in {doc_name}")
                total_stats.documents_skipped += 1
                continue

            # Write output
            output_path = output_dir / f"{doc_name}.bioes"
            output_text = format_bioes_output(sentences)
            output_path.write_text(output_text, encoding="utf-8")

            # Aggregate stats
            total_stats.documents_processed += 1
            total_stats.total_tokens += doc_stats.total_tokens
            total_stats.total_annotations += doc_stats.total_annotations
            total_stats.total_sentences += doc_stats.total_sentences
            for label, count in doc_stats.annotations_by_type.items():
                total_stats.annotations_by_type[label] = (
                    total_stats.annotations_by_type.get(label, 0) + count
                )

            print(
                f"    → {doc_stats.total_tokens} tokens, "
                f"{doc_stats.total_annotations} annotations, "
                f"{doc_stats.total_sentences} sentences"
            )

    return total_stats


def process_single_xmi(
    xmi_path: Path,
    typesystem_path: Path,
    output_dir: Path,
    annotation_types: list[str],
    type_feature: Optional[str] = None,
) -> ConversionStats:
    """Process a single XMI file with a separate typesystem file."""
    _require_cassis()
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(typesystem_path, "rb") as ts_file:
        typesystem = load_typesystem(ts_file)

    with open(xmi_path, "rb") as xmi_file:
        cas = load_cas_from_xmi(xmi_file, typesystem=typesystem)

    sentences, stats = convert_cas_to_bioes(cas, annotation_types, type_feature)

    if sentences:
        doc_name = xmi_path.stem
        output_path = output_dir / f"{doc_name}.bioes"
        output_text = format_bioes_output(sentences)
        output_path.write_text(output_text, encoding="utf-8")
        stats.documents_processed = 1
    else:
        stats.documents_skipped = 1

    return stats


def print_stats(stats: ConversionStats) -> None:
    """Print conversion statistics summary."""
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    print(f"Documents processed: {stats.documents_processed}")
    print(f"Documents skipped:   {stats.documents_skipped}")
    print(f"Total tokens:        {stats.total_tokens}")
    print(f"Total annotations:   {stats.total_annotations}")
    print(f"Total sentences:     {stats.total_sentences}")
    if stats.annotations_by_type:
        print("\nAnnotations by type:")
        for label, count in sorted(stats.annotations_by_type.items()):
            print(f"  {label}: {count}")
    if stats.total_tokens > 0:
        density = stats.total_annotations / stats.total_tokens * 100
        print(f"\nAnnotation density: {density:.1f}% of tokens")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert INCEpTION CAS XMI exports to BIOES format"
    )

    # ZIP mode (primary)
    parser.add_argument(
        "zip_file", nargs="?", type=Path,
        help="INCEpTION ZIP export file"
    )
    parser.add_argument(
        "annotator", nargs="?", type=str,
        help="Annotator username (subfolder in ZIP)"
    )

    # Single XMI mode (alternative)
    parser.add_argument(
        "--from-xmi", type=Path, metavar="XMI_FILE",
        help="Process a single XMI file instead of a ZIP"
    )
    parser.add_argument(
        "--typesystem", type=Path, metavar="TS_FILE",
        help="TypeSystem.xml path (required with --from-xmi)"
    )

    # Options
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--annotation-types", nargs="+", default=DEFAULT_ANNOTATION_TYPES,
        help="Annotation type names to extract"
    )
    parser.add_argument(
        "--type-feature", type=str, default=None,
        help="Feature name for annotation type label (e.g., 'Tipo')"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("CAS XMI → BIOES Converter")
    print("=" * 60)

    if args.from_xmi:
        # Single XMI mode
        if not args.typesystem:
            parser.error("--typesystem is required when using --from-xmi")
        print(f"Input XMI:    {args.from_xmi}")
        print(f"TypeSystem:   {args.typesystem}")
        print(f"Output:       {args.output_dir}")
        print()
        stats = process_single_xmi(
            args.from_xmi, args.typesystem, args.output_dir,
            args.annotation_types, args.type_feature
        )
    elif args.zip_file and args.annotator:
        # ZIP mode
        print(f"Input ZIP:    {args.zip_file}")
        print(f"Annotator:    {args.annotator}")
        print(f"Output:       {args.output_dir}")
        print()
        stats = process_zip(
            args.zip_file, args.annotator, args.output_dir,
            args.annotation_types, args.type_feature
        )
    else:
        parser.error("Provide either (zip_file + annotator) or (--from-xmi + --typesystem)")
        return  # unreachable, but satisfies type checker

    print_stats(stats)
    print(f"\nOutput saved to: {args.output_dir}")


if __name__ == "__main__":
    main()

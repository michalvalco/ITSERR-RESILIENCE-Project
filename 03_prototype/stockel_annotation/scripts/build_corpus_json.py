#!/usr/bin/env python3
"""
Build corpus.json for the ITSERR-RESILIENCE web prototype.

Parses normalized text files from the Stöckel annotation pipeline and
produces a structured JSON file suitable for the web-based text browser.

Applies enhanced rule-based detection for biblical, patristic, reformation,
and classical references beyond what normalize_text.py already tags.

Usage:
    python build_corpus_json.py [--input-dir DIR] [--output FILE]
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


DEFAULT_INPUT_DIR = Path(__file__).parent.parent / "data" / "normalized"
DEFAULT_OUTPUT = Path(__file__).parent.parent.parent.parent / "docs" / "prototype" / "data" / "corpus.json"

# Chapter metadata with page ranges and descriptions
CHAPTERS = [
    {"id": "title-page", "title": "TITULUS", "title_en": "Title Page", "start_page": 1, "end_page": 1},
    {"id": "praefatio", "title": "PRAEFATIO", "title_en": "Preface", "start_page": 2, "end_page": 6},
    {"id": "de-deo", "title": "DE DEO", "title_en": "On God", "start_page": 7, "end_page": 11},
    {"id": "de-trinitate", "title": "DE TRINITATE", "title_en": "On the Trinity", "start_page": 12, "end_page": 16},
    {"id": "de-spiritu-sancto", "title": "DE SPIRITU SANCTO", "title_en": "On the Holy Spirit", "start_page": 17, "end_page": 22},
    {"id": "de-creatione", "title": "DE CREATIONE", "title_en": "On Creation", "start_page": 23, "end_page": 30},
    {"id": "de-providentia", "title": "DE PROVIDENTIA", "title_en": "On Divine Providence", "start_page": 31, "end_page": 34},
    {"id": "de-libero-arbitrio", "title": "DE LIBERO ARBITRIO", "title_en": "On Free Will", "start_page": 35, "end_page": 46},
    {"id": "de-peccato", "title": "DE PECCATO", "title_en": "On Sin", "start_page": 47, "end_page": 56},
    {"id": "de-lege", "title": "DE LEGE", "title_en": "On the Law", "start_page": 57, "end_page": 58},
]

# Enhanced biblical reference patterns (broader than normalize_text.py)
# Uses [.:]? instead of \.? to handle both period and colon separators
# found in Stöckel's text (e.g., "Rom. 5" and "Actor: 20")
BIBLICAL_PATTERNS = [
    # Old Testament
    (r'\b(Gen(?:esis|es|ef)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Exod(?:us|i)?[.:]?\s*(?:X+V*I*V*X*[.:]?\s*\d*))', 'biblical'),
    (r'\b(Levit(?:icus)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Numer[.:]?\s*\d+)', 'biblical'),
    (r'\b(Deut(?:eronomij|eronom(?:ij)?)?[.:]?\s*(?:\d+|[XVI]+[.:]?))', 'biblical'),
    (r'\b(Ios(?:ue)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Iudic(?:um)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Ruth[.:]?\s*\d+)', 'biblical'),
    (r'\b((?:1|2|I|II)[.:]?\s*(?:Sam(?:uel)?|Reg(?:um)?)[.:]?\s*\d+)', 'biblical'),
    (r'\b((?:1|2|I|II)[.:]?\s*Paralip[.:]?\s*\d+)', 'biblical'),
    (r'\b(Esdr(?:ae)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Iob[.:]?\s*\d+)', 'biblical'),
    (r'\b(Psal(?:m|mo)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Pfal(?:m|mo)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),  # OCR variant
    (r'\b(Prou(?:erb)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Eccles(?:iastes)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Cant(?:ica)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Isa(?:iae|ie)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Esai(?:ae|e)?[.:]?\s*\d+)', 'biblical'),  # Variant spelling
    (r'\b(Hierem(?:iae)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Ezech(?:iel(?:is|e)?)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Dan(?:iel(?:is)?)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Osee[.:]?\s*\d+)', 'biblical'),
    (r'\b(Ioel[.:]?\s*\d+)', 'biblical'),
    (r'\b(Amos[.:]?\s*\d+)', 'biblical'),
    (r'\b(Mich(?:aeae)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Zachar(?:iae)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Malach(?:iae)?[.:]?\s*\d+)', 'biblical'),
    # New Testament
    (r'\b(Matt?h?(?:aei|ei)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Marc(?:i)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Luc(?:ae|a)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Ioan(?:nis|nem|n)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Iohan(?:nis|nem|n)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Act(?:orum|or)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Aclorum[.:]?\s*(?:X+V*I*V*X*[.:]?\s*\d*))', 'biblical'),  # OCR variant
    (r'\b(Rom(?:anos|an)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Ront[.:]?\s*\d+)', 'biblical'),  # OCR variant
    (r'\b(Genef[.:]?\s*\d+)', 'biblical'),  # OCR variant of Genesis
    (r'\b(Genefi[.:]?\s*\d+)', 'biblical'),  # OCR variant
    (r'\b(Efaie[.:]?\s*\d+)', 'biblical'),  # OCR variant of Isaiae
    # Roman numeral citations (very common in this text)
    (r'\b(Exodi\s+X+V*I*V*X*)', 'biblical'),
    (r'\b(Deuteronomij\s+\d+)', 'biblical'),
    (r'\b(Iohannis\s+\d+)', 'biblical'),
    (r'\b(Ioannis\s+\d+)', 'biblical'),
    (r'\b(Corint[bh][.:]?\s*\d+)', 'biblical'),  # Corinthians variant
    (r'\b((?:1|2|I|II)[.:]?\s*Cor(?:inth)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Galat(?:as)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Ephe[sf](?:ios|iis)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Philip(?:penses)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Colo[sf](?:senses)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b((?:1|2|I|II)[.:]?\s*Thess(?:alonicenses)?[.:]?\s*\d+)', 'biblical'),
    (r'\b((?:1|2|I|II)[.:]?\s*Tim(?:otheum)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Tit(?:um)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Hebr(?:aeos)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b(Iacob(?:i)?[.:]?\s*\d+)', 'biblical'),
    (r'\b((?:1|2|I|II)[.:]?\s*Petr(?:i)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
    (r'\b((?:1|2|3|I|II|III)[.:]?\s*Ioan(?:nis)?[.:]?\s*\d+)', 'biblical'),
    (r'\b(Apoc(?:al(?:ypsin)?)?[.:]?\s*\d+[\.,]?\s*\d*)', 'biblical'),
]

# Patristic references
PATRISTIC_PATTERNS = [
    (r'\b(August(?:inus|ini|ino)?\.?(?:\s+de\s+\w+(?:\s+\w+)?)?)', 'patristic'),
    (r'\b(Auguf[lt](?:inus|ini|ino)?\.?)', 'patristic'),  # OCR: fl/ft for st
    (r'\b(Hieronym(?:us|i|o)?\.?)', 'patristic'),
    (r'\b(Chrysostom(?:us|i|o)?\.?)', 'patristic'),
    (r'\b(Ambros(?:ius|ii|io)?\.?)', 'patristic'),
    (r'\b(Ambrof(?:ius|ij|io)?\.?)', 'patristic'),  # OCR: f for s
    (r'\b(Cyprian(?:us|i|o)?\.?)', 'patristic'),
    (r'\b(Basilius\.?)', 'patristic'),
    (r'\b(Athanas(?:ius|ii|ij)?\.?)', 'patristic'),
    (r'\b(Origenes\.?)', 'patristic'),
    (r'\b(Tertullian(?:us|i)?\.?)', 'patristic'),
    (r'\b(Irena?e(?:us|i)?\.?)', 'patristic'),
    (r'\b(Plato(?:ne|nis)?)', 'classical'),
    (r'\b(Aristotel(?:es|is)?)', 'classical'),
    (r'\b(Cicero(?:nis)?)', 'classical'),
    (r'\b(Simonides)', 'classical'),
    (r'\b(Stoic(?:i|os|o|orum|is))', 'classical'),   # Stoic school
    (r'\b(Epicur(?:eos|eorum|cos|corum))', 'classical'),  # Epicurean school
]

# Reformation references
REFORMATION_PATTERNS = [
    (r'\b(Luther(?:us|i|o)?\.?)', 'reformation'),
    (r'\b(Melanchthon(?:is|em)?\.?)', 'reformation'),
    (r'\b(Caluin(?:us|i|o)?\.?)', 'reformation'),
    (r'\b(Zwingl(?:ius|ii)?\.?)', 'reformation'),
]

# Confessional document references
# Uses [Ssf] to handle OCR long-s variant (fymbolo for symbolo)
CONFESSIONAL_PATTERNS = [
    (r'\b((?:in\s+)?[Ssf]ymbolo\s+(?:Niceno|Athanasij|Atbanaftj|Ambrosij|Ambrofij|Apostolorum))', 'confessional'),
    (r'\b(Confessio(?:nem|nis|ne)?\s+August(?:anam|anae)?)', 'confessional'),
]


def parse_page_number(text):
    """Extract page number from a [Page N] marker."""
    m = re.search(r'\[Page\s+(\d+)\]', text)
    return int(m.group(1)) if m else None


def assign_chapter(page_num):
    """Determine which chapter a page belongs to."""
    for ch in CHAPTERS:
        if ch["start_page"] <= page_num <= ch["end_page"]:
            return ch["id"]
    # Pages between chapters (e.g., 22) — not assigned to any chapter
    return None


def strip_existing_ref_tags(text):
    """Remove existing <ref> tags from normalize_text.py so we can re-detect uniformly."""
    text = re.sub(r'<ref type="[^"]*">', '', text)
    text = re.sub(r'</ref>', '', text)
    text = re.sub(r'<!-- CHAPTER: [^>]* -->\n?', '', text)
    text = re.sub(r'<chapter title="[^"]*">\n?', '', text)
    return text


def detect_references(text, crf_entities=None):
    """
    Find all references in a text segment.
    Returns list of {start, end, text, type, confidence, epistemic, methods, consensus}.

    Args:
        text: The text to scan for references.
        crf_entities: Optional list of CRF-detected entities, each a dict with
            {start, end, text, type, confidence}. When provided, references
            detected by both rule-based and CRF methods receive a "consensus"
            flag and higher epistemic confidence.

    Epistemic status assignment logic:
        - FACTUAL: ≥2 methods agree (consensus), OR well-formed biblical pattern
          with chapter/verse number (confidence ≥0.85), OR confessional document
          reference (confidence ≥0.80).
        - INTERPRETIVE: Single detection method with moderate confidence (0.70–0.85).
          Rule-based match of a name pattern without verse numbers, or CRF-only
          detection.
        - DEFERRED: Methods disagree on type, or confidence <0.70. Requires human
          annotator review. (Not yet generated — will appear when CRF layer is
          integrated and produces conflicting classifications.)
    """
    refs = []
    seen_spans = set()

    all_patterns = BIBLICAL_PATTERNS + PATRISTIC_PATTERNS + REFORMATION_PATTERNS + CONFESSIONAL_PATTERNS

    for pattern, ref_type in all_patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            start, end = m.start(), m.end()
            matched = m.group(0).strip()

            # Skip if overlapping with existing ref
            span_key = (start, end)
            if any(s <= start < e or s < end <= e for s, e in seen_spans):
                continue

            # Assign epistemic indicator based on detection quality
            # Rule-based detection alone = moderate confidence
            confidence = 0.75
            epistemic = "INTERPRETIVE"
            methods = ["rule-based"]
            consensus = False

            # Higher confidence for well-formed patterns with numbers
            if ref_type == "biblical" and re.search(r'\d', matched):
                confidence = 0.85
                epistemic = "FACTUAL"
            elif ref_type == "confessional":
                confidence = 0.80
                epistemic = "FACTUAL"

            # Check for CRF consensus if CRF entities are provided
            if crf_entities:
                overlapping = [
                    crf_ent for crf_ent in crf_entities
                    if (start <= crf_ent["start"] < end
                        or crf_ent["start"] <= start < crf_ent["end"])
                ]
                if overlapping:
                    methods.append("CRF")
                    # Prefer a CRF entity that matches the rule-based type
                    matching = [e for e in overlapping if e.get("type") == ref_type]
                    if matching:
                        best = matching[0]
                        consensus = True
                        confidence = max(confidence, best.get("confidence", 0.80))
                        confidence = min(round(confidence + 0.05, 2), 0.99)
                        epistemic = "FACTUAL"
                    else:
                        # Methods disagree on type — deferred
                        epistemic = "DEFERRED"
                        confidence = min(confidence, 0.65)

            refs.append({
                "start": start,
                "end": end,
                "text": matched,
                "type": ref_type,
                "confidence": round(confidence, 2),
                "epistemic": epistemic,
                "methods": methods,
                "method": " + ".join(methods),
                "consensus": consensus
            })
            seen_spans.add(span_key)

    # Also include CRF-only detections not covered by rules
    if crf_entities:
        for crf_ent in crf_entities:
            crf_s, crf_e = crf_ent["start"], crf_ent["end"]
            # Check if already covered by a rule-based match
            already_covered = any(
                s <= crf_s < e or crf_s <= s < crf_e
                for s, e in seen_spans
            )
            if not already_covered:
                crf_conf = crf_ent.get("confidence", 0.75)
                refs.append({
                    "start": crf_s,
                    "end": crf_e,
                    "text": crf_ent.get("text", text[crf_s:crf_e]),
                    "type": crf_ent.get("type", "unknown"),
                    "confidence": round(crf_conf, 2),
                    "epistemic": "FACTUAL" if crf_conf >= 0.85 else ("INTERPRETIVE" if crf_conf >= 0.70 else "DEFERRED"),
                    "methods": ["CRF"],
                    "method": "CRF",
                    "consensus": False
                })
                seen_spans.add((crf_s, crf_e))

    # Sort by position
    refs.sort(key=lambda r: r["start"])
    return refs


def parse_normalized_files(input_dir):
    """Parse all normalized text files and build corpus structure."""
    files = sorted(input_dir.glob("annotationes_pp*.txt"), key=lambda f: extract_sort_key(f.name))

    pages = {}

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")

        # Strip the header
        if '---' in content:
            content = content.split('---', 1)[1]

        # Split into pages
        page_blocks = re.split(r'(\[Page\s+\d+\])', content)

        current_page = None
        for block in page_blocks:
            page_num = parse_page_number(block)
            if page_num is not None:
                current_page = page_num
                continue

            if current_page is None:
                continue

            # Clean up the text
            text = block.replace('[PAGE BREAK]', '').strip()
            text = strip_existing_ref_tags(text)

            # Remove OCR garbage lines (very short lines of noise)
            lines = text.split('\n')
            clean_lines = []
            for line in lines:
                stripped = line.strip()
                # Skip lines that are mostly non-alpha noise
                if stripped and len(stripped) > 2:
                    alpha_ratio = sum(1 for c in stripped if c.isalpha()) / len(stripped)
                    if alpha_ratio > 0.4 or len(stripped) > 20:
                        clean_lines.append(stripped)
                elif not stripped:
                    clean_lines.append('')

            text = '\n'.join(clean_lines).strip()
            # Collapse multiple blank lines
            text = re.sub(r'\n{3,}', '\n\n', text)

            if not text or len(text) < 10:
                continue

            # Detect references
            refs = detect_references(text)

            # Assign chapter
            chapter_id = assign_chapter(current_page)

            pages[current_page] = {
                "page": current_page,
                "chapter_id": chapter_id,
                "text": text,
                "references": refs,
            }

    return pages


def extract_sort_key(filename):
    """Extract numeric sort key from filename like annotationes_pp1-5.txt."""
    m = re.search(r'pp(\d+)', filename)
    return int(m.group(1)) if m else 0


def build_corpus(input_dir):
    """Build the complete corpus JSON structure."""
    pages = parse_normalized_files(input_dir)

    # Build chapter objects with their pages
    chapters = []
    for ch in CHAPTERS:
        ch_pages = []
        total_refs = {"biblical": 0, "patristic": 0, "reformation": 0, "classical": 0, "confessional": 0}

        for pg_num in range(ch["start_page"], ch["end_page"] + 1):
            if pg_num in pages:
                pg = pages[pg_num]
                ch_pages.append(pg)
                for ref in pg["references"]:
                    ref_type = ref["type"]
                    if ref_type in total_refs:
                        total_refs[ref_type] += 1

        chapters.append({
            "id": ch["id"],
            "title": ch["title"],
            "title_en": ch["title_en"],
            "start_page": ch["start_page"],
            "end_page": ch["end_page"],
            "pages": ch_pages,
            "reference_counts": total_refs,
        })

    # Compute global stats
    all_refs = []
    for ch in chapters:
        for pg in ch["pages"]:
            all_refs.extend(pg["references"])

    ref_type_counts = {}
    for ref in all_refs:
        t = ref["type"]
        ref_type_counts[t] = ref_type_counts.get(t, 0) + 1

    epistemic_counts = {}
    for ref in all_refs:
        e = ref["epistemic"]
        epistemic_counts[e] = epistemic_counts.get(e, 0) + 1

    # Detection method statistics
    method_counts = {}
    consensus_count = 0
    for ref in all_refs:
        for m in ref.get("methods", [ref.get("method", "rule-based")]):
            method_counts[m] = method_counts.get(m, 0) + 1
        if ref.get("consensus", False):
            consensus_count += 1

    corpus = {
        "metadata": {
            "title": "Annotationes in Locos communes",
            "title_full": "Annotationes in Philippi Melanchthonis Locos Praecipuos Theologicos",
            "author": "Leonard Stöckel",
            "date": 1561,
            "language": "lat",
            "pages_total": len(pages),
            "publisher": "Ioannem Oporinum, Basel",
            "source": "OCR extraction via Tesseract 5.3.4",
            "pipeline": "ITSERR-RESILIENCE normalization + rule-based detection",
            "generated": datetime.now().isoformat(),
        },
        "stats": {
            "total_references": len(all_refs),
            "by_type": ref_type_counts,
            "by_epistemic": epistemic_counts,
            "by_method": method_counts,
            "consensus_count": consensus_count,
            "chapters": len(chapters),
            "pages_with_content": len(pages),
        },
        "entity_types": [
            {"id": "biblical", "label": "Biblical Citation", "color": "#2196F3", "description": "Direct reference to Scripture"},
            {"id": "patristic", "label": "Patristic Reference", "color": "#9C27B0", "description": "Reference to Church Fathers"},
            {"id": "reformation", "label": "Reformation Source", "color": "#FF9800", "description": "Reformation-era theological source"},
            {"id": "classical", "label": "Classical Reference", "color": "#607D8B", "description": "Greek/Roman classical source"},
            {"id": "confessional", "label": "Confessional Document", "color": "#4CAF50", "description": "Creedal or confessional reference"},
        ],
        "epistemic_types": [
            {"id": "FACTUAL", "label": "Factual", "color": "#4CAF50", "description": "High confidence: well-formed pattern with ≥2 confirming signals"},
            {"id": "INTERPRETIVE", "label": "Interpretive", "color": "#FF9800", "description": "Moderate confidence: single detection method, needs expert review"},
            {"id": "DEFERRED", "label": "Deferred", "color": "#F44336", "description": "Low confidence or ambiguous: requires human judgment"},
        ],
        "chapters": chapters,
    }

    return corpus


def main():
    parser = argparse.ArgumentParser(description="Build corpus.json for the web prototype")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    print(f"Reading normalized texts from: {args.input_dir}")
    corpus = build_corpus(args.input_dir)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"Corpus written to: {args.output}")
    print(f"  Chapters: {corpus['stats']['chapters']}")
    print(f"  Pages: {corpus['stats']['pages_with_content']}")
    print(f"  References: {corpus['stats']['total_references']}")
    print(f"  By type: {corpus['stats']['by_type']}")
    print(f"  By epistemic: {corpus['stats']['by_epistemic']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Text Normalization Script for Stöckel's Annotationes in Locos communes (1561)

Cleans OCR output, normalizes Latin spelling, expands abbreviations,
and marks structural elements for annotation in INCEpTION.

Usage:
    python normalize_text.py [--input-dir DIR] [--output-dir DIR] [--report]
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


# Configuration
DEFAULT_INPUT_DIR = Path(__file__).parent.parent / "data" / "cleaned"
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "data" / "normalized"


@dataclass
class NormalizationStats:
    """Track normalization changes for reporting."""
    noise_removed: int = 0
    et_normalized: int = 0
    abbreviations_expanded: int = 0
    long_s_fixed: int = 0
    chapters_found: list = field(default_factory=list)
    lemma_markers: int = 0
    total_words_before: int = 0
    total_words_after: int = 0


# =============================================================================
# OCR NOISE REMOVAL
# =============================================================================

def remove_ocr_noise(text: str, stats: NormalizationStats) -> str:
    """Remove OCR artifacts and noise from the text."""
    original = text

    # First, protect page markers from being mangled
    # Convert [Page X] to a protected token
    page_markers = re.findall(r'\[Page\s+\d+\]', text)
    for i, marker in enumerate(page_markers):
        text = text.replace(marker, f'__PAGE_MARKER_{i}__')

    # Also protect [PAGE BREAK]
    text = text.replace('[PAGE BREAK]', '__PAGE_BREAK__')

    # Pattern for page header junk (random characters at start of pages)
    # e.g., "E E em |", "M. Mh — — — néaan an:", etc.
    header_noise_patterns = [
        r'^[A-Z]\s+[A-Z]\s+\w{2,4}\s*\|.*$',  # "E E em |" pattern
        r'^[MmDdWw]\.\s+[A-Za-z]+\s*—.*$',     # "M. Mh —" pattern
        r'^[\|\!\[\]\{\}]+\s*$',                # Lines of only punctuation
        r'^\s*[\|\!\[\]]+\s*$',                 # Lines with only pipe/bracket
        r'^[—\-]+\s*[\w\s]{0,10}$',             # Dash-heavy lines
        r'^\s*[A-Z]\s*$',                       # Single letter lines
        r'^[^\w\s]{3,}$',                       # Lines of symbols
        r'^[A-Z]{2,}\s*$',                      # All caps short lines (likely headers)
        r'^\s*\d+\s*$',                         # Just page numbers
        r'^.*HERERR.*$',                        # OCR garbage patterns
        r'^.*UPIERCCA.*$',                      # More OCR garbage
        r'^[A-Za-z]{1,3}\s*$',                  # Very short random lines
    ]

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # Don't process lines with our protected markers
        if '__PAGE_MARKER_' in line or '__PAGE_BREAK__' in line:
            cleaned_lines.append(line)
            continue

        # Skip lines that match noise patterns (but not structural markers)
        is_noise = False
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            cleaned_lines.append(line)
            continue

        for pattern in header_noise_patterns:
            if re.match(pattern, stripped):
                is_noise = True
                stats.noise_removed += 1
                break

        if not is_noise:
            cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    # Remove inline noise (but protect brackets around page markers)
    inline_noise_patterns = [
        (r'\s*\|\s*', ' '),                     # Pipe characters
        (r'(?<!_)\[(?!Page)', ' '),             # Opening brackets (not [Page)
        (r'(?<!Page\s\d)\](?!_)', ' '),         # Closing brackets (not Page X])
        (r'\s*\!\s*(?![A-Z])', ' '),            # Exclamation marks (not sentence-initial)
        (r'\s*[—–-]{2,}\s*', ' '),              # Multiple dashes
        (r'(?<![_\d])\s{2,}(?![_\d])', ' '),    # Multiple spaces
    ]

    for pattern, replacement in inline_noise_patterns:
        matches = len(re.findall(pattern, text))
        stats.noise_removed += matches
        text = re.sub(pattern, replacement, text)

    # Clean up line-final random characters (but not in markers)
    text = re.sub(r'(?<!_)\s+[A-Za-z]\s*$', '', text, flags=re.MULTILINE)

    # Remove isolated punctuation clusters
    text = re.sub(r'(?<!\w)[^\w\s_]{3,}(?!\w)', '', text)

    # Restore page markers
    for i, marker in enumerate(page_markers):
        text = text.replace(f'__PAGE_MARKER_{i}__', marker)
    text = text.replace('__PAGE_BREAK__', '[PAGE BREAK]')

    return text


# =============================================================================
# LATIN ABBREVIATION EXPANSION
# =============================================================================

# Common Latin abbreviations in 16th-century texts
ABBREVIATIONS = {
    # Tironian et and variants
    r'\bez\b': 'et',
    r'\bcz\b': 'et',
    r'\be\s*z\b': 'et',

    # que abbreviation (appears as q; or similar)
    r'\bq;\b': 'que',
    r'\bq\s*;\b': 'que',
    r'q;': 'que',

    # Common theological abbreviations
    r'\bDñs\b': 'Dominus',
    r'\bDñm\b': 'Dominum',
    r'\bDño\b': 'Domino',
    r'\bDñi\b': 'Domini',
    r'\bXpi\b': 'Christi',
    r'\bXpo\b': 'Christo',
    r'\bXpm\b': 'Christum',
    r'\bXps\b': 'Christus',

    # Ecclesiastical
    r'\beccl\.\b': 'ecclesia',
    r'\bEccl\.\b': 'Ecclesia',
    r'\bepi\.\b': 'episcopus',
    r'\bEpi\.\b': 'Episcopus',

    # Common word endings
    r'(\w+)q;\s': r'\1que ',

    # etc. and similar
    r'\b&c\.\b': 'etc.',
    r'\bec\.\b': 'etc.',
}


def expand_abbreviations(text: str, stats: NormalizationStats) -> str:
    """Expand common Latin abbreviations."""
    # Track Tironian et separately
    tironian_patterns = [r'\bez\b', r'\bcz\b', r'\be\s*z\b']

    for pattern, expansion in ABBREVIATIONS.items():
        if pattern in tironian_patterns:
            matches = len(re.findall(pattern, text))
            stats.et_normalized += matches
            text = re.sub(pattern, expansion, text)
        else:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            stats.abbreviations_expanded += matches
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)

    return text


# =============================================================================
# LONG S (ſ) CORRECTION
# =============================================================================

# Words where medial/final 'f' should be 's' (OCR misread long s)
# Context-based patterns for common Latin words
LONG_S_PATTERNS = [
    # Common -ss- words (OCR'd as -fs-)
    (r'\bpofsi', 'possi'),        # possit, possum, etc.
    (r'\bpoffun', 'possun'),      # possunt
    (r'\bpoffet', 'posset'),
    (r'\bneceffa', 'necessa'),    # necessarius, etc.
    (r'\bneceffi', 'necessi'),
    (r'\bdifcip', 'discip'),      # disciplina
    (r'\bdifput', 'disput'),      # disputatio
    (r'\bdiftin', 'distin'),      # distinctio
    (r'\bdiftinc', 'distinc'),
    (r'\bdifsim', 'dissim'),      # dissimilis
    (r'\beffent', 'essent'),
    (r'\befse', 'esse'),
    (r'\beffi', 'essi'),
    (r'\beffic', 'essic'),        # but keep efficax
    (r'\bmiffio', 'missio'),
    (r'\bremifsi', 'remissi'),
    (r'\btranfgre', 'transgre'),
    (r'\bproficif', 'proficis'),

    # Words ending in -is (OCR'd as -if)
    (r'(\w{3,})if\b', r'\1is'),   # Generic -is endings

    # Common -st- patterns
    (r'\bconfti', 'consti'),      # constitutio
    (r'\binftitu', 'institu'),    # institutio
    (r'\bfubftan', 'substan'),    # substantia
    (r'\bfubfti', 'substi'),
    (r'\binftruc', 'instruc'),
    (r'\binftrumen', 'instrumen'),

    # Common -sp- patterns
    (r'\bfpiritu', 'spiritu'),    # spiritus
    (r'\bfpeci', 'speci'),        # species
    (r'\bfpecta', 'specta'),
    (r'\bfperare', 'sperare'),

    # Common -sc- patterns
    (r'\bfcien', 'scien'),        # scientia
    (r'\bfcrip', 'scrip'),        # scriptura
    (r'\bfcand', 'scand'),
    (r'\bfchol', 'schol'),        # schola

    # Initial s- (OCR'd as f-)
    (r'\bfed\b', 'sed'),
    (r'\bfic\b', 'sic'),
    (r'\bfint\b', 'sint'),
    (r'\bfunt\b', 'sunt'),
    (r'\bfit\b', 'sit'),
    (r'\bfua\b', 'sua'),
    (r'\bfuo\b', 'suo'),
    (r'\bfuum\b', 'suum'),
    (r'\bfuam\b', 'suam'),
    (r'\bfuis\b', 'suis'),
    (r'\bfibi\b', 'sibi'),
    (r'\bfimul\b', 'simul'),
    (r'\bfimil', 'simil'),        # similis
    (r'\bfine\b', 'sine'),
    (r'\bfanct', 'sanct'),        # sanctus
    (r'\bfalut', 'salut'),        # salutaris
    (r'\bfalv', 'salv'),          # salvatio
    (r'\bfapien', 'sapien'),      # sapientia
    (r'\bfatis\b', 'satis'),
    (r'\bfecund', 'secund'),      # secundum
    (r'\bfemper\b', 'semper'),
    (r'\bfent', 'sent'),          # sententia
    (r'\bfequi', 'sequi'),        # sequitur
    (r'\bferui', 'serui'),        # servitium (keeping u/v)
    (r'\bferu', 'seru'),
    (r'\bfignif', 'signif'),      # significat
    (r'\bfolid', 'solid'),
    (r'\bfolum\b', 'solum'),
    (r'\bfolu\b', 'solu'),
    (r'\bfpirit', 'spirit'),
    (r'\bftudi', 'studi'),        # studium
    (r'\bfubiec', 'subiec'),      # subiectum
    (r'\bfuffic', 'suffic'),      # sufficiens
    (r'\bfumm', 'summ'),          # summa
    (r'\bfuper', 'super'),

    # Medial -fs- → -ss-
    (r'(\w)fsi(\w)', r'\1ssi\2'),
    (r'(\w)fse(\w)', r'\1sse\2'),

    # -us/-is endings
    (r'(\w{2,})uf\b', r'\1us'),

    # Common patterns at end of words
    (r'ofum\b', 'osum'),
    (r'efum\b', 'esum'),
    (r'ifum\b', 'isum'),
]


def fix_long_s(text: str, stats: NormalizationStats) -> str:
    """Fix long s (ſ) OCR'd as f in Latin words."""
    for pattern, replacement in LONG_S_PATTERNS:
        matches = len(re.findall(pattern, text, re.IGNORECASE))
        stats.long_s_fixed += matches
        # Preserve case for first character
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


# =============================================================================
# STRUCTURAL ELEMENT MARKING
# =============================================================================

# Chapter/section patterns in the Annotationes
# Order matters - more specific patterns first
CHAPTER_PATTERNS = [
    (r'\bDE\s+PECCATO\s+ORIG(?:INIS|INALI)?', 'DE PECCATO ORIGINIS'),
    (r'\bDE\s+IVSTIFICATIONE\b', 'DE IUSTIFICATIONE'),
    (r'\bDE\s+IUSTIFICATIONE\b', 'DE IUSTIFICATIONE'),
    (r'\bDE\s+LEGE\s+ET\s+EVANGELIO\b', 'DE LEGE ET EVANGELIO'),
    (r'\bDE\s+LIBERO\s+ARBITRIO\b', 'DE LIBERO ARBITRIO'),
    (r'\bDE\s+SPIRITV\s+SANCTO\b', 'DE SPIRITU SANCTO'),
    (r'\bDE\s+SPIRITU\s+SANCTO\b', 'DE SPIRITU SANCTO'),
    (r'\bDE\s+CREATIONE[EF]?\b', 'DE CREATIONE'),
    (r'\bDE\s+DEO\b', 'DE DEO'),
    (r'\bDE\s+TRINITATE\b', 'DE TRINITATE'),
    (r'\bDE\s+PROVIDENTIA\b', 'DE PROVIDENTIA'),
    (r'\bDE\s+PECCATO\b', 'DE PECCATO'),
    (r'\bDE\s+LEGI[OÓ]\b', 'DE LEGE'),
    (r'\bDE\s+LEGE\b', 'DE LEGE'),
    (r'\bPRAEFATIO\b', 'PRAEFATIO'),
    (r'\bPRÀEFATIO\b', 'PRAEFATIO'),
    (r'\bDB[\.:]\s*PECCATO\b', 'DE PECCATO'),  # OCR error variant
]


def mark_structural_elements(text: str, stats: NormalizationStats) -> str:
    """Identify and mark chapter breaks and structural elements."""

    # Find and normalize chapter titles
    for pattern, normalized in CHAPTER_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Check if this is a chapter heading (usually in page header or standalone)
            context_start = max(0, match.start() - 50)
            context_end = min(len(text), match.end() + 50)
            context = text[context_start:context_end]

            # If it looks like a heading (after page marker or at line start)
            if re.search(r'(\[Page \d+\]|\n)\s*' + pattern, text, re.IGNORECASE):
                if normalized not in stats.chapters_found:
                    stats.chapters_found.append(normalized)

    # Mark chapter headings with XML-like tags for INCEpTION
    for pattern, normalized in CHAPTER_PATTERNS:
        # Only mark standalone chapter headings (not inline references)
        text = re.sub(
            r'(\[Page \d+\]\s*\n?)(' + pattern + r')(\s*\n)',
            r'\1<!-- CHAPTER: ' + normalized + r' -->\n<chapter title="' + normalized + r'">\n\2\3',
            text,
            flags=re.IGNORECASE
        )

    return text


def identify_lemma_boundaries(text: str, stats: NormalizationStats) -> str:
    """
    Mark potential lemma boundaries in commentary text.

    Lemmas in theological commentaries are often:
    - Biblical citations (e.g., "Rom. 5", "Psalm 51")
    - Theological terms being glossed
    - Latin phrases in small caps or italics (lost in OCR)
    """

    # Biblical reference patterns
    bible_patterns = [
        r'\b(Gen(?:esis|ef)?\.?\s*\d+)',
        r'\b(Exod(?:us)?\.?\s*\d+)',
        r'\b(Psalm\.?\s*\d+)',
        r'\b(Pfal(?:m)?\.?\s*\d+)',  # OCR variant
        r'\b(Psal(?:m)?\.?\s*\d+)',
        r'\b(Rom(?:anos)?\.?\s*\d+)',
        r'\b(Matt?h?(?:aeus)?\.?\s*\d+)',
        r'\b(Ioan(?:nem)?\.?\s*\d+)',
        r'\b(Iohan(?:nem)?\.?\s*\d+)',
        r'\b(Act(?:orum)?\.?\s*\d+)',
        r'\b(Ephe[sf]\.?\s*\d+)',
        r'\b(Galat\.?\s*\d+)',
        r'\b(Hierem\.?\s*\d+)',
        r'\b(Isa(?:iae)?\.?\s*\d+)',
        r'\b(Ezech(?:iele)?\.?\s*\d+)',
    ]

    for pattern in bible_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        stats.lemma_markers += len(matches)
        # Mark biblical references
        text = re.sub(
            pattern,
            r'<ref type="biblical">\1</ref>',
            text,
            flags=re.IGNORECASE
        )

    # Patristic reference patterns
    patristic_patterns = [
        r'\b(August(?:inus|ini)?\.?)',
        r'\b(Hieronym(?:us|i)?\.?)',
        r'\b(Chrysostom(?:us|i)?\.?)',
        r'\b(Ambros(?:ius|ii)?\.?)',
        r'\b(Cyprian(?:us|i)?\.?)',
    ]

    for pattern in patristic_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        stats.lemma_markers += len(matches)
        text = re.sub(
            pattern,
            r'<ref type="patristic">\1</ref>',
            text,
            flags=re.IGNORECASE
        )

    # Reformation-era references
    reformation_patterns = [
        r'\b(Luther(?:us|i)?)',
        r'\b(Melanchthon(?:is)?)',
        r'\b(Caluin(?:us|i)?)',
        r'\b(Philippus)',  # Often refers to Melanchthon
    ]

    for pattern in reformation_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        stats.lemma_markers += len(matches)
        text = re.sub(
            pattern,
            r'<ref type="reformation">\1</ref>',
            text,
            flags=re.IGNORECASE
        )

    return text


# =============================================================================
# MAIN NORMALIZATION PIPELINE
# =============================================================================

def normalize_text(text: str, stats: Optional[NormalizationStats] = None) -> str:
    """
    Apply full normalization pipeline to OCR text.

    Pipeline order:
    1. Remove OCR noise
    2. Expand abbreviations
    3. Fix long s → s
    4. Mark structural elements
    5. Identify lemma/reference boundaries
    """
    if stats is None:
        stats = NormalizationStats()

    stats.total_words_before = len(text.split())

    # 1. Remove noise
    text = remove_ocr_noise(text, stats)

    # 2. Expand abbreviations
    text = expand_abbreviations(text, stats)

    # 3. Fix long s
    text = fix_long_s(text, stats)

    # 4. Mark structural elements
    text = mark_structural_elements(text, stats)

    # 5. Identify lemma boundaries
    text = identify_lemma_boundaries(text, stats)

    # Final cleanup
    text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
    text = re.sub(r'[ \t]+', ' ', text)      # Single spaces
    text = re.sub(r' +\n', '\n', text)       # No trailing spaces

    stats.total_words_after = len(text.split())

    return text


def process_file(input_path: Path, output_path: Path, stats: NormalizationStats) -> None:
    """Process a single file through the normalization pipeline."""
    print(f"Processing: {input_path.name}")

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split header from content
    if '---' in content:
        parts = content.split('---', 1)
        header = parts[0] + '---\n'
        text = parts[1] if len(parts) > 1 else ''
    else:
        header = ''
        text = content

    # Normalize
    normalized = normalize_text(text, stats)

    # Add normalization metadata to header
    norm_header = f"""# Normalized: {datetime.now().isoformat()}
# Normalization: spelling, abbreviations, structural markup
"""

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header + norm_header + '\n' + normalized)

    print(f"  → Saved: {output_path.name}")


def generate_report(stats: NormalizationStats, output_path: Path) -> None:
    """Generate a normalization report."""
    report = f"""# Text Normalization Report
Generated: {datetime.now().isoformat()}

## Summary Statistics

| Metric | Count |
|--------|-------|
| Noise characters removed | {stats.noise_removed} |
| 'et' normalized (ez/cz) | {stats.et_normalized} |
| Abbreviations expanded | {stats.abbreviations_expanded} |
| Long s (ſ→s) fixed | {stats.long_s_fixed} |
| Reference markers added | {stats.lemma_markers} |
| Words before | {stats.total_words_before} |
| Words after | {stats.total_words_after} |

## Chapters Identified

"""
    if stats.chapters_found:
        for chapter in stats.chapters_found:
            report += f"- {chapter}\n"
    else:
        report += "- No chapter markers found\n"

    report += """
## Normalization Decisions

### Spelling Normalization
- `ez`, `cz` → `et` (Tironian et symbol)
- Long s (ſ) appearing as `f` → `s` in appropriate contexts
- Common Latin word patterns corrected

### Abbreviations Expanded
- `q;` → `que`
- Common theological abbreviations (Dñs, Xpi, etc.)

### Structural Markup
- Chapter headings marked with XML comments
- Biblical references tagged with `<ref type="biblical">`
- Patristic references tagged with `<ref type="patristic">`
- Reformation-era references tagged with `<ref type="reformation">`

### Notes
- Original page markers [Page N] preserved
- Page break markers [PAGE BREAK] preserved
- OCR metadata header preserved
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Normalize OCR text from Stöckel's Annotationes"
    )
    parser.add_argument(
        '--input-dir', type=Path, default=DEFAULT_INPUT_DIR,
        help='Directory containing OCR text files'
    )
    parser.add_argument(
        '--output-dir', type=Path, default=DEFAULT_OUTPUT_DIR,
        help='Output directory for normalized files'
    )
    parser.add_argument(
        '--report', action='store_true',
        help='Generate normalization report'
    )
    parser.add_argument(
        '--file', type=str,
        help='Process only this specific file'
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Stöckel Annotationes - Text Normalization")
    print("=" * 60)
    print(f"Input:  {args.input_dir}")
    print(f"Output: {args.output_dir}")
    print()

    # Collect statistics
    total_stats = NormalizationStats()

    # Find input files
    if args.file:
        input_files = [args.input_dir / args.file]
    else:
        input_files = sorted(args.input_dir.glob("annotationes_pp*.txt"))

    if not input_files:
        print("No input files found!")
        return

    print(f"Found {len(input_files)} files to process\n")

    # Process each file
    for input_file in input_files:
        output_file = args.output_dir / input_file.name
        file_stats = NormalizationStats()
        process_file(input_file, output_file, file_stats)

        # Aggregate stats
        total_stats.noise_removed += file_stats.noise_removed
        total_stats.et_normalized += file_stats.et_normalized
        total_stats.abbreviations_expanded += file_stats.abbreviations_expanded
        total_stats.long_s_fixed += file_stats.long_s_fixed
        total_stats.lemma_markers += file_stats.lemma_markers
        total_stats.total_words_before += file_stats.total_words_before
        total_stats.total_words_after += file_stats.total_words_after
        total_stats.chapters_found.extend(
            c for c in file_stats.chapters_found
            if c not in total_stats.chapters_found
        )

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files processed:        {len(input_files)}")
    print(f"Noise removed:          {total_stats.noise_removed}")
    print(f"Abbreviations expanded: {total_stats.abbreviations_expanded}")
    print(f"Long s fixed:           {total_stats.long_s_fixed}")
    print(f"References marked:      {total_stats.lemma_markers}")
    print(f"Chapters found:         {len(total_stats.chapters_found)}")
    if total_stats.chapters_found:
        for chapter in total_stats.chapters_found:
            print(f"  - {chapter}")

    # Generate report if requested
    if args.report:
        report_path = args.output_dir / "NORMALIZATION_REPORT.md"
        generate_report(total_stats, report_path)

    print(f"\nOutput saved to: {args.output_dir}")


if __name__ == "__main__":
    main()

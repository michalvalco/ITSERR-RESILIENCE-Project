# Text Normalization

`normalize_text.py` normalizes OCR-extracted Latin text from 16th-century sources, handling common OCR errors, archaic typography, and Latin abbreviation conventions.

## Usage

```bash
cd 03_prototype/stockel_annotation
python scripts/normalize_text.py
```

The script processes all `.txt` files in `data/cleaned/` and writes normalized output to `data/normalized/`.

## Normalization Steps

The pipeline applies the following transformations in order:

### 1. OCR Noise Removal

Removes artifacts from OCR that are not part of the original text:

- Isolated punctuation fragments
- Non-Latin characters from misrecognized glyphs
- Control characters and zero-width spaces

### 2. Long S Correction

The long s (`ſ`) was standard in 16th-century typography but is often misrecognized by OCR as `f`:

| OCR Output | Corrected |
|------------|-----------|
| `ſicut` | `sicut` |
| `eſt` | `est` |
| `ſcriptura` | `scriptura` |

### 3. Abbreviation Expansion

Common Latin abbreviations are expanded consistently:

| Abbreviation | Expansion | Context |
|-------------|-----------|---------|
| `q;` | `que` | Enclitic conjunction |
| `ez` / `cz` | `et` | Tironian et |
| Nasal bars | Expanded | `ā` → `an`/`am` |

Matching is case-insensitive with case-preserving replacement (e.g., `Q;` → `Que`).

### 4. Ligature Expansion

Standard typographic ligatures are expanded:

| Ligature | Expanded |
|----------|----------|
| `ﬁ` | `fi` |
| `ﬂ` | `fl` |
| `ﬀ` | `ff` |

### 5. V/U Confusion Correction

In early modern Latin printing, `v` and `u` were often interchangeable. Common patterns are corrected:

| OCR Output | Corrected | Rule |
|------------|-----------|------|
| `vn` | `un` | Word-initial `vn` |
| `qvod` | `quod` | `qv` → `qu` |
| `VV` | `W` | Double-V ligature |

### 6. Structural Element Marking

Identifies and marks structural boundaries in the text:

- **Chapter breaks** — Detected via `DE [TOPIC]` patterns (e.g., `DE PECCATO ORIGINIS`)
- **Biblical references** — ~70 patterns covering the full biblical canon (OT Pentateuch through Revelation), including numbered books (e.g., `1. Cor. 13`, `2. Reg. 12`) and period/colon separator variants (`Rom. 5` and `Actor: 20`)
- **Patristic references** — Augustine, Jerome, Chrysostom, Ambrose, Cyprian
- **Reformation references** — Luther, Melanchthon, Calvin

### 7. Whitespace Normalization

- Multiple spaces collapsed to single space
- Consecutive newlines limited to 2 (paragraph breaks)
- Leading/trailing whitespace stripped from lines

## Output

Normalized files are written to `data/normalized/` with a detailed report:

- `NORMALIZATION_REPORT.md` — Statistics on all transformations applied
- `STRUCTURAL_ANALYSIS.md` — Identified chapters, references, and structural elements

## Test Suite

111 comprehensive tests cover all normalization functions:

```bash
python -m pytest tests/test_normalize_text.py -v
```

Tests cover OCR noise removal, abbreviation expansion, long-s correction, structural marking, biblical references (all canon sections including OT/NT, numbered books, separator variants), patristic references, reformation references, and case-preserving replacement.

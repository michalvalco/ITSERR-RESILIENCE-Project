# OCR Processor

`ocr_processor.py` extracts text from scanned PDF pages using Tesseract OCR with Latin language support. It supports three output formats: plaintext, ALTO XML, or both.

## Usage

```bash
# Plaintext only (default, backward-compatible)
python scripts/ocr_processor.py

# Specific page range
python scripts/ocr_processor.py --pages 1-10

# ALTO XML output
python scripts/ocr_processor.py --format alto --pages 1-10

# Both plaintext and ALTO XML in a single pass
python scripts/ocr_processor.py --format both --pages 1-10 --single-file

# Custom output directories
python scripts/ocr_processor.py --format both --output-dir data/cleaned/ --alto-dir data/alto/
```

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--pages` | `1-58` | Page range (e.g., `1-10`, `5-20`) |
| `--output-dir` | `data/cleaned/` | Directory for plaintext output |
| `--alto-dir` | `data/alto/` | Directory for ALTO XML output |
| `--format` | `txt` | Output format: `txt`, `alto`, or `both` |
| `--single-file` | off | Combine all pages into one output file |

## Output Formats

### `--format txt` (default)

Produces UTF-8 plaintext files with metadata headers and chapter detection:

```
# OCR Extracted Text
# Source: Annotationes Locorum Communium, 1561
# Pages: 1-5
# Extracted: 2026-02-13 14:30:00

De Peccato Originali
Caput I.
...
```

Text is cleaned with Latin-specific corrections:

- Long s (`ſ`) replaced with `s`
- Ligatures expanded (`ﬁ` → `fi`, `ﬂ` → `fl`)
- v/u confusion corrected for common Latin patterns (`vn` → `un`, `qvod` → `quod`)
- Whitespace normalized, excessive newlines collapsed

### `--format alto`

Produces per-page ALTO XML files preserving the full OCR structure:

```
data/alto/
├── page_001.xml
├── page_002.xml
└── ...
```

Each file contains Tesseract's native ALTO v3 output with:

- Page layout structure (PrintSpace, TextBlock, TextLine)
- Per-word content (`String/@CONTENT`)
- Per-word confidence scores (`String/@WC`)
- Hyphenation markup (`HYP`, `HypPart1`, `HypPart2`)

!!! note
    ALTO XML output is **raw** — text cleaning (long-s, ligatures, v/u) is deliberately not applied to preserve the original OCR structure for downstream tools.

### `--format both`

Produces both plaintext and ALTO XML in a single pass. The PDF is converted to images only once, then both `image_to_string` and `image_to_alto_xml` are called on each page image. This is more efficient than running the two formats separately.

## Python API

```python
from ocr_processor import extract_text_from_pdf, extract_alto_from_pdf, extract_both_from_pdf
from pathlib import Path

# Plaintext only
texts = extract_text_from_pdf(Path("input.pdf"), start_page=1, end_page=10)
# Returns: {1: "page 1 text...", 2: "page 2 text...", ...}

# ALTO XML only
altos = extract_alto_from_pdf(Path("input.pdf"), start_page=1, end_page=10)
# Returns: {1: b"<alto>...</alto>", 2: b"<alto>...</alto>", ...}

# Both in one pass
texts, altos = extract_both_from_pdf(Path("input.pdf"), start_page=1, end_page=10)
```

## Version Requirements

ALTO XML output requires `pytesseract >= 0.3.8` (which provides `image_to_alto_xml`). The script checks for this at startup and displays a clear error message if the method is not available:

```
error: pytesseract.image_to_alto_xml() not available.
Upgrade pytesseract: pip install --upgrade pytesseract>=0.3.8
```

## Next Step

After OCR extraction, ALTO XML files can be parsed with [`extract_alto.py`](extract-alto.md) for confidence analysis, or plaintext can be normalized with [`normalize_text.py`](normalize-text.md).

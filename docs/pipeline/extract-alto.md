# ALTO XML Parser

`extract_alto.py` parses ALTO XML files produced by Tesseract OCR and extracts clean plaintext with optional per-word OCR confidence scores. It supports both single-file and batch processing modes.

## Usage

### Single File

```bash
# Basic extraction
python scripts/extract_alto.py data/alto/page_001.xml -o output.txt

# With confidence scores
python scripts/extract_alto.py data/alto/page_001.xml -o output.txt \
    --confidence scores.csv --min-confidence 0.5

# Page range filtering
python scripts/extract_alto.py data/alto/page_001.xml -o output.txt --pages 1-5
```

### Batch Processing

```bash
# Process all ALTO XML files in a directory
python scripts/extract_alto.py data/alto/ -o data/cleaned/

# Recursive with confidence export
python scripts/extract_alto.py data/alto/ -o data/cleaned/ --recursive --export-confidence
```

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `input` | ALTO XML file or directory of XML files |
| `-o`, `--output` | Output file (single mode) or directory (batch mode) |
| `--confidence` | CSV file path for per-word confidence scores (single mode) |
| `--export-confidence` | Generate per-file confidence CSVs (batch mode) |
| `--min-confidence` | Minimum confidence threshold for flagging (default: 0.7) |
| `--pages` | Page range filter (e.g., `1-10`) |
| `--recursive` | Process subdirectories in batch mode |

## Features

### Namespace Auto-Detection

Automatically detects and handles ALTO v2.x, v3.x, and no-namespace schemas:

```xml
<!-- v3 (Tesseract default) -->
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">

<!-- v2 -->
<alto xmlns="http://www.loc.gov/standards/alto/ns-v2#">

<!-- No namespace (legacy) -->
<alto>
```

### Hyphenation Handling

Reconstructs hyphenated words split across lines using ALTO's `HYP`, `HypPart1`, and `HypPart2` elements:

```xml
<TextLine>
  <String CONTENT="theo" />
  <HYP CONTENT="-" />
</TextLine>
<TextLine>
  <String CONTENT="logica" SUBS_CONTENT="theologica" SUBS_TYPE="HypPart2" />
</TextLine>
```

Output: `theologica` (uses `SUBS_CONTENT` when available, falls back to simple concatenation)

### Confidence Score Extraction

Exports per-word OCR confidence from `String/@WC` attributes:

```csv
page,line,word,confidence
1,1,De,0.95
1,1,Peccato,0.88
1,1,Originali,0.72
```

Words below `--min-confidence` are flagged for manual review.

### Encoding Fallback

Handles non-standard ALTO files that use Latin-1 encoding despite declaring UTF-8:

1. First attempts UTF-8 parsing
2. If encoding errors detected, falls back to Latin-1
3. Logs a warning about the encoding issue

## Python API

```python
from extract_alto import extract_text_from_alto, extract_confidence_from_alto

# Extract plaintext
text = extract_text_from_alto("data/alto/page_001.xml")

# Extract with page range
text = extract_text_from_alto("data/alto/page_001.xml", page_range=(1, 5))

# Extract confidence data
confidence_data = extract_confidence_from_alto("data/alto/page_001.xml")
# Returns list of WordConfidence(page, line, word, confidence)
```

## Output Format

Plaintext output uses `[Page N]` and `[PAGE BREAK]` markers compatible with the downstream `normalize_text.py` pipeline:

```
[Page 1]
De Peccato Originali

Caput I.

Quod peccatum originis sit ...

[PAGE BREAK]
[Page 2]
...
```

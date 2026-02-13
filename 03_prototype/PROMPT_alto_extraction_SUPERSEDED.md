# PROMPT: Build ALTO XML → Pipeline-Format Extraction Script

## Context

I'm working on the ITSERR-RESILIENCE-Project, adapting the CIC_annotation pipeline
(originally for medieval Canon law) for Protestant theological texts. The CIC_annotation
pipeline currently starts from DOCX input via `split_docx.py`, but our source materials
come as digitised images with ALTO XML OCR metadata from the Slovak National Library
(DIKDA repository).

I need a script that replaces `split_docx.py` as the entry point — extracting text from
ALTO XML files and producing plaintext that feeds into the existing `cas_to_bioes.py`
conversion step (which then feeds the 6-layer annotation pipeline).

## What ALTO XML looks like

ALTO (Analyzed Layout and Text Object) XML is the OCR output format from ABBYY FineReader.
Key structure:
- `<Page>` → `<PrintSpace>` → `<TextBlock>` → `<TextLine>` → `<String>`
- Each `<String>` element has attributes:
  - `CONTENT` — the recognised word
  - `WC` — word confidence (0.0–1.0)
  - `HPOS`, `VPOS`, `WIDTH`, `HEIGHT` — bounding box coordinates
- `<SP>` elements represent spaces between words
- `<HYP>` elements represent hyphenation at line breaks

Example fragment:
```xml
<TextLine HPOS="120" VPOS="300" WIDTH="800" HEIGHT="40">
  <String CONTENT="Matt." WC="0.95" HPOS="120" VPOS="300" WIDTH="80" HEIGHT="35"/>
  <SP WIDTH="10"/>
  <String CONTENT="5,3" WC="0.88" HPOS="210" VPOS="300" WIDTH="60" HEIGHT="35"/>
  <SP WIDTH="8"/>
  <String CONTENT="Beati" WC="0.97" HPOS="278" VPOS="300" WIDTH="90" HEIGHT="35"/>
</TextLine>
```

## What the CIC_annotation pipeline expects as input

The pipeline expects **one token per line** plaintext. Looking at how `split_docx.py`
works in the CIC_annotation codebase (`C:\Users\valco\OneDrive\Documents\GitHub\CIC_annotation\`):
- It splits DOCX by chapter headings (regex: `X N.N title`)
- Outputs plain text files, one per chapter
- These text files then go into `cas_to_bioes.py` for BIOES tagging

For our adaptation, the output should be:
- Plain text with one token per line (matching what the pipeline downstream expects)
- Sentence boundaries preserved (empty line between sentences)
- Page boundaries marked (e.g., `### PAGE 5 ###` or similar marker)
- Optionally: a companion metadata file preserving confidence scores and coordinates
  per token (for the epistemological classification system downstream)

## Requirements

### Script: `alto_to_plaintext.py`

Location: `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype\src\itserr_agent\pipeline\`
(Create the `pipeline/` directory if it doesn't exist, with `__init__.py`)

**Core functionality:**
1. Parse ALTO XML files (handle both single files and directories of files)
2. Extract text content preserving reading order (TextBlock → TextLine → String)
3. Handle hyphenation at line breaks (`<HYP>` elements — rejoin hyphenated words)
4. Output one-token-per-line plaintext files
5. Preserve page/chapter structure with markers

**Confidence metadata (important for our epistemological classification):**
- Extract `WC` (word confidence) for each token
- Output a companion `.meta.tsv` file with columns: `token`, `confidence`, `page`, `line`, `hpos`, `vpos`
- This metadata feeds our FACTUAL/INTERPRETIVE/DEFERRED classification system:
  - WC ≥ 0.85 → high confidence OCR (can trust the token)
  - WC 0.70–0.85 → medium confidence (may need verification)
  - WC < 0.70 → low confidence (flag for human review)

**Handling edge cases:**
- Missing `WC` attribute → default to 0.0 (flag for review)
- Empty `<String>` elements → skip
- Nested ZIP structures (DIKDA sometimes packages ALTO XML in ZIPs)
- Multiple ALTO files per document (one per page) — stitch in page order
- File naming: sort by page number (handle both `page_001.xml` and `p1.xml` patterns)

**CLI interface:**
```
python alto_to_plaintext.py --input /path/to/alto/ --output /path/to/output/
python alto_to_plaintext.py --input single_page.xml --output page.txt
python alto_to_plaintext.py --input /path/to/alto/ --output /path/to/output/ --no-metadata
python alto_to_plaintext.py --input /path/to/alto/ --output /path/to/output/ --min-confidence 0.70
```

Options:
- `--input`: Single ALTO XML file or directory of ALTO XML files
- `--output`: Output directory (creates .txt + .meta.tsv per input file, or stitched output)
- `--stitch`: Combine all pages into a single output file (default: separate files per page)
- `--no-metadata`: Skip generating the .meta.tsv companion file
- `--min-confidence FLOAT`: Flag tokens below this threshold in output (default: 0.70)
- `--page-markers`: Include page boundary markers in output (default: True)
- `--rejoin-hyphens`: Rejoin hyphenated words across line breaks (default: True)

### Dependencies
- `lxml` for XML parsing (faster than ElementTree for large files)
- Standard library only otherwise (argparse, pathlib, csv, zipfile)
- Add `lxml` to `pyproject.toml` if not already present

### Tests: `test_alto_extraction.py`

Location: `03_prototype/tests/test_alto_extraction.py`

Include:
1. Test with a minimal synthetic ALTO XML fragment (embed in test, don't need external files)
2. Test hyphenation rejoining
3. Test confidence extraction and threshold filtering
4. Test page stitching with correct ordering
5. Test empty/malformed input handling
6. Test metadata TSV output format

### Integration notes

- This script is the **first step** in our adapted pipeline. Its output feeds into
  `cas_to_bioes.py` (from CIC_annotation) which converts to BIOES format.
- The confidence metadata feeds into our epistemological classification system
  (see `03_prototype/src/itserr_agent/epistemic/classifier.py`).
- The script should be importable as a module (for use in the agent prototype)
  AND runnable as a CLI tool (for batch processing).

### Reference files to consult

Before coding, read these for context:
- `C:\Users\valco\OneDrive\Documents\GitHub\CIC_annotation\split_docx.py` — the script this replaces
- `C:\Users\valco\OneDrive\Documents\GitHub\CIC_annotation\cas_to_bioes.py` — the downstream consumer
- `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\docs\resources\pipeline_technical_reference.md` — pipeline architecture overview
- `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\workflow_diagram.md` — Stage 2 (PARSE) section for full context

## What NOT to build

- Do NOT build OCR functionality — Tesseract/Poppler handle that separately
- Do NOT build the BIOES conversion — `cas_to_bioes.py` already exists
- Do NOT modify any CIC_annotation scripts — this is a new entry point alongside them
- Keep it simple — this is a bridge script, not a framework

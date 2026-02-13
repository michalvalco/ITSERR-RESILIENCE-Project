# PROMPT: Audit Documentation Consistency — Pipeline Status

## What happened

We discovered that three scripts in `stockel_annotation/scripts/` were already built and tested (78 tests passing), but several documentation files still described them as gaps or "TO BE BUILT." Some corrections were made in the current session, but we need a systematic check to make sure nothing was missed.

## The confirmed pipeline (ground truth)

```
PDF/TIFF/JPG/PNG → ocr_processor.py --format both → data/alto/*.xml + data/cleaned/*.txt
                                                            ↓
                                             extract_alto.py → confidence scores.csv
                                                            ↓
                                                  normalize_text.py
                                                            ↓
                                        data/normalized/*.txt → BIOES tagging → CRF pipeline
```

**Status of each component:**
- ✅ `ocr_processor.py` — supports `--format {txt,alto,both}`, Tesseract + Poppler, handles PDF/TIFF/JPG/PNG
- ✅ `extract_alto.py` — parses ALTO XML (both Tesseract and ABBYY output), extracts text + per-word confidence scores (WC attribute) into companion CSV
- ✅ `normalize_text.py` — orthographic normalization (long-s, ligatures, v/u confusion, whitespace)
- ✅ 78 tests passing across OCR and ALTO extraction modules
- The CIC_annotation pipeline (6-layer: Rules → Abbreviations → Match → CRF → Structure → Merge) is the *downstream* consumer — it exists in a separate repo and is NOT being modified, only adapted via new rule sets, abbreviation dictionaries, and retraining

**Key facts:**
- `ocr_processor.py` does OCR *and* produces ALTO XML in one step — no need for a separate ALTO extraction step from OCR
- `extract_alto.py` is for *parsing existing* ALTO XML (e.g., ABBYY FineReader output from DIKDA) into plaintext + confidence CSV — it's complementary, not redundant
- Input formats: PDF, TIFF, JPG, PNG all handled by Tesseract/Poppler
- The ALTO XML → pipeline-format gap that was identified earlier is **closed**

## Files to audit

Read each of these files and check for any language that:
- Says the ALTO XML extraction "does not exist yet" or is "TO BE BUILT"
- Describes `split_docx.py` as the only entry point (the Stöckel path uses our new scripts)
- Lists text extraction as a gap or open question
- Shows outdated pipeline diagrams (e.g., missing the three scripts, showing "?" for extraction)
- References the superseded prompt `PROMPT_alto_extraction.md` (renamed to `_SUPERSEDED`)

### Primary documents to check:

1. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\workflow_diagram.md`
2. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\pipeline_overview.mermaid`
3. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\pipeline_stage4_deep_dive.mermaid`
4. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\docs\resources\pipeline_technical_reference.md`
5. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\TNA_FELLOWSHIP_HUB.md`

### Secondary documents (also check if they exist):

6. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\docs\resources\integrated_report_strategy.md`
7. `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype\stockel_annotation\scripts\GNORM_PIPELINE_ANALYSIS.md`
8. Any README files in `03_prototype/` or `stockel_annotation/`

### Also verify the scripts themselves exist:

9. Confirm these three files are present and non-empty:
   - `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype\stockel_annotation\scripts\ocr_processor.py`
   - `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype\stockel_annotation\scripts\extract_alto.py`
   - `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype\stockel_annotation\scripts\normalize_text.py`

### Mermaid diagrams — specific checks:

For `pipeline_overview.mermaid`:
- Stage 2 (PARSE) should show `ocr_processor.py --format both` as the OCR step, not just "ABBYY/Transkribus"
- The format annotation between Stage 2 and Stage 3 should show the dual output (ALTO XML + plaintext)
- `extract_alto.py` and `normalize_text.py` should appear in Stage 2
- No "TO BE BUILT" markers on extraction steps

For `pipeline_stage4_deep_dive.mermaid`:
- The INPUT section should reference normalized plaintext coming from `normalize_text.py`, not raw ALTO XML
- Confidence scores from `extract_alto.py` should be shown feeding into the epistemological classification section
- Check that the BIOES format description is consistent with what `cas_to_bioes.py` actually expects

## What to do

1. Read all listed files
2. For each file, report: filename, any inconsistencies found (quote the problematic text), and proposed fix
3. Apply the fixes (edit the files directly)
4. After all edits, list a summary of changes made

## What NOT to do

- Don't restructure or rewrite documents beyond what's needed for consistency
- Don't modify any Python scripts — only documentation files
- Don't delete `PROMPT_alto_extraction_SUPERSEDED.md` (keep it as an audit trail)
- Don't change the pipeline_technical_reference.md PKB description of the CIC_annotation pipeline itself — that documents the *original* CIC pipeline accurately; only update references to *our* Stöckel adaptation pipeline

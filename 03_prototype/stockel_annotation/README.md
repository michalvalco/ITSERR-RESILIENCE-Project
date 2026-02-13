# Stöckel Corpus Annotation Pilot Study

**Status:** Active Development (Fellowship Phase)
**Principal Investigator:** Michal Valčo
**Context:** ITSERR/RESILIENCE Transnational Access Fellowship
**Timeline:** Preparation before Feb 10, 2026 → Execution during fellowship

---

## Overview

This sub-project adapts the GNORM annotation pipeline to Leonard Stöckel's 16th-century theological works, testing whether CRF-based reference extraction can generalize from medieval canon law to Reformation-era Protestant commentaries.

### Research Question

**Can GNORM's CRF approach generalize to 16th-century Protestant theological texts?**

### Why Stöckel?

1. **Dense Citation Networks:** The *Annotationes in Locos communes* (1561) contains extensive references to Patristic, Biblical, Classical, and contemporary Reformation sources
2. **Structural Similarity:** Medieval glosses and Reformation commentaries share abbreviated citation formats, marginal apparatus structures, and *allegationes* logic
3. **Research Gap:** No automated annotation system exists for Reformation-era theological commentaries

---

## Directory Structure

```
stockel_annotation/
├── README.md              # This file
├── PROGRESS.md            # Detailed progress tracking
├── CHAPTER_SELECTION.md   # Rationale for chapter selection
├── data/
│   ├── raw/               # Original PDF and OCR output
│   ├── cleaned/           # OCR-extracted text files (12 files, ~18,900 words)
│   ├── alto/              # ALTO XML output from Tesseract (per-page XML)
│   ├── normalized/        # Text after normalization pipeline
│   └── annotations/       # INCEpTION exports (manual annotations)
├── models/
│   ├── gnorm_baseline/    # Reference GNORM model for comparison
│   └── stockel_crf/       # Domain-adapted CRF model
├── scripts/
│   ├── ocr_processor.py   # Tesseract OCR extraction (txt, ALTO XML, or both)
│   ├── extract_alto.py    # ALTO XML parser → plaintext + confidence scores
│   ├── normalize_text.py  # Text normalization (abbreviations, long-s, structure)
│   └── GNORM_PIPELINE_ANALYSIS.md  # Analysis of GNORM's CRF pipeline
├── tools/
│   └── inception/         # INCEpTION setup and annotation configuration
└── results/
    └── experiments.md     # Documented findings
```

---

## Selected Test Texts

| Text | Date | Genre | Citation Density | Status |
|------|------|-------|------------------|--------|
| *Annotationes in Locos communes* (2-3 chapters) | 1561 | Commentary | High | Pending selection |
| *Catechesis* | 1556 | Catechism | Medium | Baseline comparison |
| *Postilla* (selected passages) | 1598 | Homiletical | Variable | Genre comparison |

---

## Annotation Schema

Adapted from GNORM for theological texts:

| Entity Type | GNORM Equivalent | Stöckel Application |
|-------------|------------------|---------------------|
| Glossed lemma | `Lemma glossato` | Commented biblical/theological term |
| Legal reference | `Allegazione normativa` | Patristic/biblical citation |
| Title | `Titolo` | Work referenced (e.g., *De Civitate Dei*) |
| Chapter | `Capitolo` | Specific passage location |
| **NEW:** Biblical reference | — | Scripture citations (book:chapter:verse) |
| **NEW:** Contemporary reference | — | Reformation-era sources (Luther, Melanchthon) |

---

## Experiment Plan

### Experiment 1: Direct Transfer
- Run GNORM's trained model on Stöckel text (zero-shot)
- Evaluate: What does it find? What does it miss?
- Hypothesis: Will identify some patristic citations but miss biblical references

### Experiment 2: Retrained CRF
- Train new CRF using manual Stöckel annotations
- Compare simple vs. rich feature configurations
- Document performance vs. GNORM's Liber Extra baseline

### Experiment 3: Hybrid Approach
- Combine GNORM's pre-trained features with domain-specific additions
- Test whether knowledge transfer from canon law helps
- Evaluate cross-domain generalization

---

## OCR & ALTO XML Pipeline

The project includes a two-stage OCR pipeline for extracting structured text from 16th-century PDF scans:

### Stage 1: `ocr_processor.py` — PDF to Text/ALTO

Extracts text from PDF using Tesseract OCR with Latin language support.

```bash
# Plaintext only (default, backward-compatible)
python scripts/ocr_processor.py --format txt

# ALTO XML only (structured XML with per-word confidence)
python scripts/ocr_processor.py --format alto --alto-dir data/alto/

# Both plaintext and ALTO XML in a single pass
python scripts/ocr_processor.py --format both
```

Features: Latin-specific text cleaning (long-s, ligatures, v/u confusion), chapter detection, configurable page ranges, single-file or per-page output.

### Stage 2: `extract_alto.py` — ALTO XML to Plaintext + Confidence

Parses ALTO XML files (v2.x/v3.x) to produce clean plaintext with optional per-word OCR confidence scores.

```bash
# Single file
python scripts/extract_alto.py data/alto/page_001.xml -o output.txt --confidence scores.csv

# Batch processing (all XML in directory)
python scripts/extract_alto.py data/alto/ -o data/cleaned/ --export-confidence --recursive
```

Features: hyphenation handling, namespace auto-detection, encoding fallback (UTF-8 → Latin-1), page range filtering, batch processing with confidence CSV export.

### Test Coverage

| Test Suite | Tests | File |
|------------|-------|------|
| OCR processor | 34 | `tests/test_ocr_processor.py` |
| ALTO parser | 55 | `tests/test_extract_alto.py` |
| Text normalizer | 74 | `tests/test_normalize_text.py` |

---

## Related Resources

- **GNORM Repository:** https://github.com/aesuli/CIC_annotation
- **Zenodo Dataset:** DOI 10.5281/zenodo.14381709
- **INCEpTION:** https://inception-project.github.io/
- **CRFsuite:** https://www.chokkan.org/software/crfsuite/

---

## Progress Tracking

See **[PROGRESS.md](PROGRESS.md)** for detailed checklist and status updates.

---

*Part of the ITSERR Transnational Access Fellowship project*
*Last updated: February 13, 2026*

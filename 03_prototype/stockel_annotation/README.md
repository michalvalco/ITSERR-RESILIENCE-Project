# Stöckel Corpus Annotation Pilot Study

**Status:** Pre-Fellowship Preparation Phase
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
├── PROGRESS.md            # Detailed progress tracking (pre-fellowship checklist)
├── data/
│   ├── raw/               # Original OCR output from Stöckel texts
│   ├── cleaned/           # Preprocessed, normalized text files
│   └── annotations/       # INCEpTION exports (manual annotations)
├── models/
│   ├── gnorm_baseline/    # Reference GNORM model for comparison
│   └── stockel_crf/       # Domain-adapted CRF model
├── scripts/
│   ├── preprocess.py      # Text cleaning and normalization
│   ├── train_crf.py       # CRF model training
│   └── evaluate.py        # Performance metrics
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
*Last updated: January 25, 2026*

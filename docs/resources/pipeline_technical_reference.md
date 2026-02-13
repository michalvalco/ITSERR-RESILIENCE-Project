# Pipeline Technical Reference: CIC_annotation / GNORM Adaptation

**Purpose:** Static reference card for Claude Project PKB. Quick-lookup for any technical conversation about the annotation pipeline and its adaptation for Protestant theological texts.  
**Source:** Condensed from `CIC_annotation_Deep_Dive_Report.md` (567 lines), `workflow_diagram.md` (358 lines), `epistemic_modesty_framework.md`, and direct code inspection.  
**Last updated:** February 13, 2026

---

## 1. Pipeline Architecture Overview

The CIC_annotation pipeline is a **six-layer hybrid system**, not a monolithic CRF. Each layer contributes annotations independently; a merge step resolves conflicts using **first-method-wins priority** (Layer 1 > 2 > ... > 4).

| Layer | Script | Method | What It Detects |
|-------|--------|--------|-----------------|
| 1 | `annotate_by_rule.py` | Trie + regex | Structured legal patterns (e.g., `NUM.q.NUM,`) |
| 2 | `annotate_by_abbreviations.py` | Dictionary lookup | Known abbreviation sequences |
| 3 | `annotate_by_match.py` | Trie exact + statistical gap prediction | Previously seen patterns; `PREPOST` fills gaps within mean ± 2σ |
| 4 | `annotate_by_crfsuite.py` | CRF machine learning | General reference patterns (the 97.8% accuracy layer) |
| 5 | `annotate_chapter.py` / `annotate_title.py` / `annotate_lemma.py` | Structural regex | Document structure (chapters, titles, glossed lemmas) |
| 6 | `merge_annotations.py` + `post_process.py` | Merge + correction | Unified output with `mark_source` provenance labels |

✅ **Key insight:** Rules and dictionaries override the CRF when they fire — precision over recall by design.  
✅ **Performance:** 97.8% accuracy (CRF rich config), 41,784 legal references, 1.1 MB model, 21 min training on desktop CPU.  
✅ **Codebase:** ~1,200 lines Python across 16 files. CC BY 4.0 license.

---

## 2. Data Formats and Flow

### BIOES Tagging Scheme

Code uses **BIOES**; paper says **BILOU**. Same scheme, different names:

| Code (BIOES) | Paper (BILOU) | Meaning |
|:---:|:---:|---|
| B | B | Beginning of multi-token entity |
| I | I | Inside multi-token entity |
| E | L | End/Last of multi-token entity |
| O | O | Outside any entity |
| S | U | Single-token entity |

Label format: `{SOURCE|}TAG-TYPE` — e.g., `CRF|B-AN`, `RULE|S-AN`, `O`

### INCEpTION Roundtrip

```
INCEpTION export (ZIP-within-ZIP, UIMA CAS XMI + TypeSystem.xml)
    → cas_to_bioes.py → BIOES plaintext (one token per line)
    → pipeline processing (6 layers)
    → bioes_to_cas.py → UIMA CAS XMI (with source in Tipo field)
    → import back to INCEpTION for expert review
```

✅ `cas_to_bioes.py`: Reads nested ZIP structure. Annotation type: `webanno.custom.Glossa`, feature `Tipo`. Handles per-user annotations (multi-annotator support).  
✅ `bioes_to_cas.py`: TypeSystem is **hardcoded in the script** (not loaded externally). Supports 4 entity types.

### Current Input Format

CIC pipeline starts from **manually transcribed DOCX** (`split_docx.py`), NOT from OCR. The DOCX is split by chapter headings via regex (`X N.N title`).  
✅ **For Stöckel:** ALTO XML → plaintext extraction pipeline built: `ocr_processor.py --format both` → `extract_alto.py` → `normalize_text.py` (78 tests passing). Located in `stockel_annotation/scripts/`.

---

## 3. Entity Types

### Current CIC Types (4)

| Type | BIOES Suffix | Detection Method |
|------|:---:|---|
| Allegazione normativa (legal reference) | `AN` | Layers 1–4 (rules, abbrev, match, CRF) |
| Lemma glossato (glossed lemma) | `LEMMA` | Layer 5 (`annotate_lemma.py`) |
| Capitolo (chapter) | `CHAPTER` | Layer 5 (`annotate_chapter.py`) |
| Titolo (title) | `TITLE` | Layer 5 (`annotate_title.py`) |

✅ Only `AN` is ML-learned. `LEMMA`, `CHAPTER`, `TITLE` use structural regex.

### Proposed Protestant Adaptation (7)

| Entity Type | Proposed Suffix | Example | CIC Parallel | Detection Strategy |
|---|:---:|---|---|---|
| Biblical_citation | `BIBLICAL` | *Matt. 5,3–12* | AN | Rules + CRF |
| Patristic_reference | `PATRISTIC` | *Aug. de civ. Dei XIV.28* | AN | Rules + CRF |
| Confessional_reference | `CONFESSIONAL` | *CA Art. IV* | AN | Rules + CRF |
| Hymnological_reference | `HYMN` | *Cithara Sanctorum No. 42* | (new) | Rules + CRF |
| Cross_reference | `XREF` | *vid. supra cap. III* | (new) | Rules |
| Glossed_term | `GLOSSED` | *iustificatio, fides* | LEMMA | Structural |
| Section_header | `SECTION` | *Caput III: De fide* | CHAPTER/TITLE | Structural |

❓ **Open:** Can the CRF handle all 7 types simultaneously, or separate models per type?  
❓ **Open:** Annotation boundary — reference string only, or reference + framing context?

---

## 4. Feature Engineering and CRF

### Window and Features

- **Window:** ±6 tokens (code: `window_size = 6`; total = 13 tokens including target)
- **Paper says** "context window of size seven" — discrepancy, likely counting convention

**Features per token:**
- `bias` (constant), raw form, lowercase, `isupper`, `istitle`, `isdigit`
- Boundary markers: `__BOS__` (beginning), `__EOS__` (end of sentence)
- Number normalization: all digits → `__NUM__`
- Context prefix: `pw1`–`pw6` (previous words), `nw1`–`nw6` (next words)

**N-gram features:** bigrams, trigrams, skip-grams over full 13-token window (`ngram_max_size = 3`)

✅ **What's NOT included:** No character-level features (no char n-grams, no prefix/suffix). Significant gap for historical orthographic variation (ſ/s, ij/j, cz/č, w/v, ß/ss).

### Hyperparameter Search

| Parameter | Value |
|---|---|
| Algorithm | L-BFGS |
| CV | 5-fold |
| Iterations | 100 (RandomizedSearchCV) |
| Scoring | F1 macro |
| Parallelization | `cpu_count() // 2 - 1` cores |
| L1 regularization (`c1`) | `expon(scale=0.5)` |
| L2 regularization (`c2`) | `expon(scale=0.05)` |
| Transitions | `all_possible_transitions: [True, False]` |
| States | `all_possible_states: [True, False]` |

### Library

✅ `sklearn-crfsuite` wrapping `python-crfsuite` (CRFsuite by Okazaki).  
⚠️ **Last PyPI release: 2017.** Unmaintained. Functional but sustainability risk for 48-month project.  
Model serialized as Python **pickle** (version-locked; portability concern).

---

## 5. Source Tracking and Epistemological Classification

### The `mark_source` Mechanism

When enabled, every annotation carries a provenance prefix:

| Prefix | Source | Layer |
|---|---|:---:|
| `SOURCE\|` | Expert annotation (training data) | — |
| `RULE\|` | Rule-based detection | 1 |
| `ABBREVIATION\|` | Abbreviation dictionary | 2 |
| `MATCH\|` | Exact trie matching | 3 |
| `PREPOST\|` | Statistical gap prediction | 3 |
| `CRF\|` | CRF model | 4 |

✅ Preserved in INCEpTION roundtrip via `Tipo` field (e.g., `Allegazione normativa|CRF`).

### Dual-Path Epistemological Classification

Combines **method consensus** (across pipeline layers) with **CRF marginal probabilities** (`predict_marginals()`):

| Classification | Method Consensus Criterion | CRF Confidence | Action |
|---|---|---|---|
| **FACTUAL** | ≥2 methods agree, OR `MATCH` (exact pattern) | ≥ 0.85 | Accept; include in public dataset |
| **INTERPRETIVE** | CRF alone, OR `PREPOST` (statistical) | 0.70–0.85 | Flag for expert review |
| **DEFERRED** | Methods disagree, OR ambiguous | < 0.70, OR theological judgment needed | Route to human annotator |

```python
# CRF marginal probabilities (not used in original CIC code, proposed addition):
y_marginals = model.predict_marginals(X)
for token_marginals in sentence_marginals:
    confidence = max(token_marginals.values())
    best_label = max(token_marginals, key=token_marginals.get)
```

❓ **Open:** `predict_marginals()` may produce poorly calibrated probabilities. May need Platt scaling or isotonic regression.  
✅ **Design principle:** Dual-path is more robust than either mechanism alone. This is a genuine methodological contribution beyond the original CIC design.

---

## 6. Dependencies and Environment

| Package | Purpose | Status |
|---|---|---|
| `dkpro-cassis` | UIMA CAS XMI processing (INCEpTION format) | ✅ Active |
| `scikit-learn` | ML infrastructure | ✅ Active |
| `sklearn-crfsuite` | CRF implementation | ⚠️ Unmaintained since 2017 |
| `python-docx` | DOCX input parsing | ✅ Active |

- No GPU required. Desktop CPU sufficient.
- Model size: 1.1 MB (pickle format).
- Training: 21 minutes on desktop CPU (CIC corpus).
- Migration path if needed: `python-crfsuite` directly (maintained) or PyTorch CRF layers.

---

## 7. Adaptation Gaps

### Per-Layer Adaptation Requirements

| Layer | Current (CIC) | Needed (Protestant) | Effort | Status |
|---|---|---|---|---|
| Rules | Canon law citation regex | Biblical/patristic/confessional regex | Medium | 🔧 Needs building |
| Abbreviations | Legal abbreviation dictionary | Theological abbreviation dictionary | Medium | 🔧 Needs building |
| Match model | CIC training trie | Retrain on Protestant patterns | Low | 🔧 After training data |
| CRF | CIC-trained, word-level features | Retrain; add character-level features | Medium-High | 🔧 Core technical work |
| Structural | CIC chapter/title regex | 16th-c. printed book structure | Medium | 🔧 Needs building |
| Post-processing | "ff." correction only | Domain-specific corrections (TBD from error analysis) | Low | 🔧 After zero-shot test |

### Additional Infrastructure Gaps

| Gap | Description | Effort | Status |
|---|---|---|---|
| ALTO XML → plaintext | CIC starts from DOCX; our sources are TIFF + ALTO XML | Medium | ✅ Built (`ocr_processor.py` → `extract_alto.py` → `normalize_text.py`; 78 tests passing) |
| Character-level features | Historical orthographic variation (ſ/s, cz/č, etc.) | Medium | 🔧 Not started |
| Multilingual handling | Latin/German/Czech code-switching within documents | High | 🔧 Not started |
| OCR error impact | Unknown error rates on 16th-c. print | ❓ | Needs empirical testing |
| 3D visualization | Mentioned in ITSERR docs; absent from CIC_annotation code | ❓ | Separate GNORM component? |
| Multi-entity CRF | Current CRF handles only one ML entity type (AN) | ❓ | Ask Arianna |

---

## 8. Key Open Questions

### ✅ Confirmed (from code analysis + Feb 12 meeting)

- CRF library: `sklearn-crfsuite`
- Output format: BIOES → UIMA CAS XMI
- Feature set: word-level, ±6 window, bigrams + trigrams
- Hyperparameters: L-BFGS, 5-fold CV, 100 iterations, F1 macro
- Post-processing: single "ff." rule
- Pipeline architecture: 6-layer hybrid (not just CRF)
- Workflow framework: Fry 2007 (Acquire → Parse → Filter → Mine → Represent → Refine → Interact)

### ❓ Still TBD (for Arianna/Marcello meetings)

- Zero-shot test on Stöckel sample (not yet conducted)
- Multi-entity type CRF performance vs. separate models
- Match model `pre_post_len = 3` — was this optimized?
- ~~ALTO XML integration~~ — ✅ Resolved: `ocr_processor.py` → `extract_alto.py` → `normalize_text.py` (78 tests passing)
- 3D visualization component — what does it expect as input?
- Gospel passage detection examples from CIC paper (empirical anchor for adaptation thesis)
- Minimum training set size for acceptable CRF performance
- `predict_marginals()` calibration quality
- Merge priority alternatives (confidence-based? majority voting?)
- INCEpTION annotation protocol for Protestant types (not yet drafted)
- Inter-annotator agreement thresholds

---

## Quick Reference: File → Function

| Script | What It Does | Adaptation Impact |
|---|---|:---:|
| `train_crfsuite.py` | CRF training + hyperparameter search | **HIGH** |
| `annotate_by_crfsuite.py` | CRF inference | LOW |
| `train_match_model.py` | Build trie models from training data | MODERATE |
| `annotate_by_match.py` | Trie + statistical matching | MODERATE |
| `annotate_by_rule.py` | Rule-based detection | **HIGH** |
| `annotate_by_abbreviations.py` | Abbreviation dictionary lookup | **HIGH** |
| `annotate_chapter.py` | Chapter structure detection | **HIGH** |
| `annotate_title.py` | Title structure detection | **HIGH** |
| `annotate_lemma.py` | Glossed lemma positioning | MODERATE |
| `cas_to_bioes.py` | INCEpTION → BIOES | LOW |
| `bioes_to_cas.py` | BIOES → INCEpTION (hardcoded TypeSystem) | MODERATE |
| `merge_annotations.py` | Multi-method merge | LOW |
| `post_process.py` | Error correction ("ff." rule) | **HIGH** |
| `build_annotations_index.py` | Cross-reference index builder | **HIGH** |
| `statistics.py` | Annotation count reports | LOW |
| `split_docx.py` | DOCX preprocessing | **HIGH** (replaced by `ocr_processor.py` → `extract_alto.py` → `normalize_text.py` for Stöckel path) |
| `trie.py` | Trie data structure (utility) | NONE |

---

*Reference card for Claude Project PKB. For full analysis see `CIC_annotation_Deep_Dive_Report.md` in APVV repo. For current project status see `TNA_FELLOWSHIP_HUB.md`.*

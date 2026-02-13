# PROMPT: Create Pipeline Technical Reference for Claude Project PKB

**Purpose:** Produce a static reference document (~200–250 lines) that gives Claude immediate context for any technical conversation about the CIC_annotation / GNORM pipeline and its adaptation for Protestant theological texts.

**Output file:** `pipeline_technical_reference.md`  
**Destination:** Upload to Claude Project PKB after creation. Also save a copy in `GitHub\ITSERR-RESILIENCE-Project\docs\resources\`.  
**After upload:** Update Claude Project Instructions to list this file in the PKB Contents section.

---

## What to Read Before Writing

Read these files from the filesystem in this order:

1. **CIC_annotation Deep Dive** (authoritative, 567 lines):  
   `C:\Users\valco\OneDrive\Documents\GitHub\APVV-2026-Religiozne-Dedicstvo\06_technologie\CIC_annotation_Deep_Dive_Report.md`  
   — Sections 1.1 (pipeline architecture), 1.2 (dependencies), 1.5 (BIOES format), 1.6 (source tracking → epistemological classification), 1.7 (INCEpTION roundtrip)

2. **Workflow Diagram** (7 stages, 358 lines):  
   `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\workflow_diagram.md`  
   — Stages 2–4 (Parse, Filter, Mine) are most relevant. Entity type schema proposal is in Stage 3.

3. **Epistemic Modesty Framework**:  
   `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\epistemic_modesty_framework.md`  
   — The FACTUAL / INTERPRETIVE / DEFERRED classification and how it maps to pipeline outputs.

4. **CIC_annotation source code** (skim for structure confirmation):  
   `C:\Users\valco\OneDrive\Documents\GitHub\CIC_annotation\`  
   — Key files: `annotate_by_rule.py`, `annotate_by_crfsuite.py`, `merge_annotations.py`, `cas_to_bioes.py`, `bioes_to_cas.py`, `train_crfsuite.py`

---

## Document Structure (proposed)

### 1. Pipeline Architecture Overview (~30 lines)
The 6-layer pipeline with table: Layer → Script → Method → What It Detects.  
Merge priority logic (Layer 1 > Layer 2 > ... > Layer 4).  
Key insight: this is a hybrid pipeline, not just a CRF.

### 2. Data Formats and Flow (~25 lines)
BIOES tagging scheme (with BILOU equivalence table).  
Input formats: ALTO XML, plaintext, DOCX (current).  
INCEpTION roundtrip: CAS XMI → BIOES → pipeline → BIOES → CAS XMI.  
The ZIP-within-ZIP export format.

### 3. Entity Types (~25 lines)
Current CIC types (4): Allegazione normativa, Lemma glossato, Capitolo, Titolo.  
Proposed Protestant adaptation (7): Biblical_citation, Patristic_reference, Confessional_reference, Hymnological_reference, Cross_reference, Glossed_term, Section_header.  
Mapping table showing CIC parallels.

### 4. Feature Engineering and CRF (~25 lines)
Window size (6+1+6 = 13 tokens). Feature set per token.  
N-gram features (bigrams, trigrams, skip-grams).  
What's NOT included: character-level features (needed for historical orthographic variation).  
Hyperparameter search: L-BFGS, 5-fold CV, 100 iterations, F1 macro.  
Library: sklearn-crfsuite (no longer maintained but functional).

### 5. Source Tracking and Epistemological Classification (~30 lines)
The `mark_source` mechanism: SOURCE|, CRF|, MATCH|, PREPOST|, RULE|, ABBREVIATION|.  
Dual-path classification: method consensus + CRF marginal probabilities.  
Mapping table: FACTUAL (≥2 methods agree AND confidence ≥0.85) / INTERPRETIVE (CRF alone OR 0.70–0.85) / DEFERRED (disagreement OR <0.70 OR theological judgment required).  
Note on calibration: predict_marginals() may need Platt scaling.

### 6. Dependencies and Environment (~15 lines)
4 Python packages: dkpro-cassis, scikit-learn, sklearn-crfsuite, python-docx.  
Model serialization: pickle (portability concern).  
CRF model size: 1.1 MB, trains in 21 minutes on desktop CPU.

### 7. Adaptation Gaps (~30 lines)
What needs building per layer (table from workflow diagram Stage 4).  
ALTO XML → plaintext extraction (doesn't exist yet).  
Character-level features for historical orthography.  
Multilingual handling (Latin/German/Czech switches within documents).  
OCR error rates on 16th-century print (unknown, requires empirical testing).

### 8. Key Open Questions (~15 lines)
Confirmed vs. TBD from Arianna/Marcello meetings.  
Zero-shot test status.  
INCEpTION annotation protocol (not yet drafted).  
Inter-annotator agreement thresholds.

---

## Writing Guidelines

- **Density over elegance.** This is a reference card, not a narrative document. Tables, code snippets, and terse descriptions preferred.
- **No overlap with other PKB files.** The literature landscape (Source A) covers the scholarly context. The reference mapping covers the agent prototype. This document covers only the CIC/GNORM pipeline and its adaptation.
- **Actionable specifics.** Include actual script names, actual feature names, actual format details. Claude should be able to answer "What format does INCEpTION export?" or "What features does the CRF use?" directly from this document without reading the Deep Dive.
- **Mark what's confirmed vs. assumed.** Use ✅ for confirmed facts, ❓ for open questions, and 🔧 for "needs building."
- **Target: ~200–250 lines.** If it goes longer, cut the least actionable content.

---

## Post-Creation Checklist

- [ ] Save to `GitHub\ITSERR-RESILIENCE-Project\docs\resources\pipeline_technical_reference.md`
- [ ] Upload to Claude Project PKB
- [ ] Update Claude Project Instructions PKB Contents section to include the new file
- [ ] Update HUB's "Claude Project PKB Contents" table
- [ ] Append session log entry to `integrated_report_strategy.md` Section 8

# Stöckel Annotation Experiments

**Status:** Pre-experiment preparation phase (baseline expectations defined)
**Last Updated:** January 25, 2026

---

## Experiment Overview

Three planned experiments to evaluate GNORM's CRF pipeline generalization to Reformation-era theological texts.

---

## Baseline: GNORM Performance on Liber Extra

Based on analysis of the Zenodo dataset (DOI: 10.5281/zenodo.14381709):

| Metric | Value | Source |
|--------|-------|--------|
| Total documents | 186 | Complete corpus |
| Expert-annotated documents | 39 | High-quality subset |
| Total annotation tokens | 18,425 | Expert annotations |
| Unique legal references | 462 | Distinct citations |
| Average annotations/document | 472.4 | Expert set |
| Highest density document | `2.02 DE FORO COMPETENTI` | 3,943 annotations |

### Annotation Format

- **Format:** WebAnno TSV 3.3
- **Label:** `Allegazione normativa[N]` (legal reference with ID)
- **Schema:** Token-level annotation with character offsets

### Reference Document for Comparison

The document `2.02 DE FORO COMPETENTI` provides an excellent reference for understanding dense citation patterns in the GNORM corpus.

---

## Experiment 1: Direct Transfer (Zero-Shot)

**Objective:** Evaluate GNORM's pre-trained model on Stöckel text without any adaptation.

### Setup
- **Model:** GNORM's trained CRF model (from *Liber Extra* corpus)
- **Test data:** Selected Stöckel chapters
- **Metrics:** Precision, Recall, F1-score per entity type

### Hypothesis
The model will:
- ✓ Identify some patristic citations (similar format to legal citations)
- ✗ Miss biblical references (different format, abbreviations)
- ✗ Struggle with vernacular (German) embedded text
- ? Handle contemporary Reformation references

### Results

| Entity Type | Precision | Recall | F1 | Notes |
|-------------|-----------|--------|----|----|
| Patristic citations | — | — | — | — |
| Biblical citations | — | — | — | — |
| Classical citations | — | — | — | — |
| Contemporary refs | — | — | — | — |

**Observations:**
- (To be completed during fellowship)

---

## Experiment 2: Retrained CRF

**Objective:** Train new CRF model using manual Stöckel annotations.

### Setup
- **Training data:** Manual annotations (target: 100+ references)
- **Features:** Simple vs. rich feature configuration
- **Baseline:** GNORM's *Liber Extra* performance (462 unique refs in 39 expert docs)
- **Expected challenge:** Smaller training set vs. GNORM's 18,425 annotation tokens

### Configurations to Test

| Config | Features | Description |
|--------|----------|-------------|
| Simple | Word, position | Minimal feature set |
| Medium | + POS tags, case | Standard NER features |
| Rich | + character n-grams, abbreviation patterns | Domain-specific features |

### Results

| Config | Precision | Recall | F1 | Training Time |
|--------|-----------|--------|----|----|
| Simple | — | — | — | — |
| Medium | — | — | — | — |
| Rich | — | — | — | — |

**Observations:**
- (To be completed during fellowship)

---

## Experiment 3: Hybrid Approach

**Objective:** Combine GNORM's pre-trained features with domain-specific additions.

### Setup
- **Base:** GNORM feature representations
- **Additions:** Biblical abbreviation patterns, Reformation-era authority names
- **Hypothesis:** Knowledge transfer from canon law improves performance

### Results

| Approach | Precision | Recall | F1 | Notes |
|----------|-----------|--------|----|----|
| GNORM-only | — | — | — | Baseline from Exp 1 |
| Stöckel-only | — | — | — | From Exp 2 |
| Hybrid | — | — | — | Combined approach |

**Observations:**
- (To be completed during fellowship)

---

## Error Analysis Template

### Common Error Types

| Error Type | Example | Frequency | Potential Fix |
|------------|---------|-----------|---------------|
| — | — | — | — |

### Annotation Disagreements

| Case | Gold Label | Prediction | Resolution |
|------|------------|------------|------------|
| — | — | — | — |

---

## Success Criteria

### Minimum Viable Success
- [ ] Direct transfer identifies >20% of patristic citations
- [ ] Retrained CRF achieves F1 >0.5 on test set
- [ ] Clear documentation of failure modes

### Target Success
- [ ] Retrained CRF achieves F1 >0.7 on theological references
- [ ] Hybrid approach outperforms single-domain models
- [ ] Annotation schema validated for Reformation texts

### Stretch Goals
- [ ] Biblical citation detection >0.8 F1
- [ ] Cross-genre generalization (Commentary → Catechism)
- [ ] Publishable results for ITSERR deliverable

---

## Conclusions

(To be written after experiments are complete)

### Key Findings
1. —
2. —
3. —

### Recommendations for Domain Adaptation
- —

### Future Work
- —

---

*Part of the ITSERR Transnational Access Fellowship project*

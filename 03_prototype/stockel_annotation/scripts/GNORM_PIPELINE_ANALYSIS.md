# GNORM Pipeline Analysis

**Date:** January 25, 2026
**Source:** https://github.com/aesuli/CIC_annotation
**Commit:** Latest (cloned to `gnorm_repo/`)

---

## Pipeline Overview

The GNORM system performs automatic annotation of legal references (*allegationes*) in the Liber Extra's Ordinary Gloss using Conditional Random Fields (CRF).

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GNORM Pipeline Flow                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [INCEpTION Export]  →  [cas_to_bioes.py]  →  [train_crfsuite.py]  │
│       (ZIP/XMI)           (BIOES format)        (CRF Model)        │
│                                                                     │
│  [New Text]  →  [annotate_by_crfsuite.py]  →  [bioes_to_cas.py]    │
│                      (Prediction)               (Back to XMI)       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Scripts

### 1. `cas_to_bioes.py` - Data Preparation

**Purpose:** Convert INCEpTION CAS XMI exports to BIOES-tagged sequences.

**Input:** ZIP file containing:
- `TypeSystem.xml` - Annotation type definitions
- `*.xmi` files - Document text + annotations

**Output:** BIOES-formatted files with tokens:
```
token start_offset end_offset label
```

**Labels:** `B-AN`, `I-AN`, `E-AN`, `S-AN`, `O`
- B = Beginning of entity
- I = Inside entity
- E = End of entity
- S = Single token entity
- O = Outside (not an entity)

**Entity Types Supported:**
- `AN` - Allegazione normativa (legal reference)
- `LEMMA` - Lemma glossato (glossed lemma)
- `CHAPTER` - Capitolo (chapter reference)
- `TITLE` - Titolo (title reference)

**Usage:**
```bash
python cas_to_bioes.py <zip_file_path> <username>
```

### 2. `train_crfsuite.py` - Model Training

**Purpose:** Train CRF model using sklearn-crfsuite.

**Features Extracted:**
- Current word features (lowercase, isupper, istitle, isdigit)
- Context window: 6 tokens before/after
- N-grams: up to 3-grams
- Number normalization (digits → `__NUM__`)
- Boundary markers: `__BOS__`, `__EOS__`

**Training Process:**
1. Load annotated BIOES files
2. Extract features for each token
3. RandomizedSearchCV for hyperparameter tuning (100 iterations, 5-fold CV)
4. L-BFGS algorithm, max 1000 iterations
5. Save model as pickle file

**Hyperparameters Tuned:**
- `c1`, `c2`: Regularization coefficients
- `all_possible_transitions`: Enable all label transitions
- `all_possible_states`: Enable all feature-label combinations

**Usage:**
```bash
python train_crfsuite.py <tagged_files_list> <zip_file_path> <username>
```

**Output:** `ner-model_YYYY-MM-DD.crfsuite.pkl`

### 3. `annotate_by_crfsuite.py` - Inference

**Purpose:** Apply trained model to new documents.

**Input:**
- Trained CRF model (pickle)
- ZIP file with unannotated documents (INCEpTION format)

**Output:** BIOES files with predicted annotations marked as `CRF|label`

**Usage:**
```bash
python annotate_by_crfsuite.py <model_file> <zip_file_path> <username>
```

### 4. `bioes_to_cas.py` - Export Back to INCEpTION

**Purpose:** Convert predicted BIOES annotations back to UIMA CAS XMI format for import into INCEpTION.

### 5. `statistics.py` - Performance Metrics

**Purpose:** Generate statistics from BIOES annotation files.

**Outputs:**
- Global counts per entity type
- Per-document statistics
- Average annotations per document

---

## Data Format Reference

### INCEpTION TypeSystem (relevant types)

```xml
<!-- Token segmentation -->
de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token
de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence

<!-- Custom annotation layer -->
webanno.custom.Glossa  <!-- Used for legal reference annotations -->
```

### WebAnno TSV 3.3 Format (Actual Zenodo Export)

**Verified from Zenodo dataset analysis (Jan 25, 2026):**

```tsv
#FORMAT=WebAnno TSV 3.3
#T_SP=webanno.custom.Glossa|Tipo

#Text=Quoniam omne quod non est ex fide, peccatum est, 28. q. 1 § quod autem
4-1    79-86     Quoniam    _
4-2    87-91     omne       _
...
4-12   128-130   28         Allegazione normativa[1]
4-13   130-131   .          Allegazione normativa[1]
4-14   132-133   q          Allegazione normativa[1]
4-15   133-134   .          Allegazione normativa[1]
4-16   135-136   1          Allegazione normativa[1]
4-17   137-138   §          Allegazione normativa[1]
4-18   139-143   quod       Allegazione normativa[1]
4-19   144-149   autem      Allegazione normativa[1]
4-20   149-150   ;          _
```

**Columns:**
1. Token ID (sentence-token format: `4-12`)
2. Character offsets (`128-130`)
3. Token text (`28`)
4. Annotation label (`_` for none, `Allegazione normativa[N]` for legal reference)

**Key observation:** The `[N]` suffix groups tokens belonging to the same reference span.

### BIOES File Format (Pipeline Output)

```
# sentence 1
Quod 0 4 O
est 5 8 O
in 9 11 B-AN
c. 12 14 I-AN
1. 15 17 E-AN

# sentence 2 (empty line separates sentences)
...
```

---

## Zenodo Dataset Statistics (Verified)

**DOI:** 10.5281/zenodo.14381709

| Dataset | Documents | Annotations |
|---------|-----------|-------------|
| Complete corpus | 186 | All formats available |
| Expert annotations | 39 | 18,425 tokens, 462 unique refs |

### Available Export Formats

| Format | Directory | Use Case |
|--------|-----------|----------|
| `conll/` | CoNLL | Standard NER format |
| `conllu/` | CoNLL-U | Universal Dependencies |
| `nif/` | NLP Interchange Format | Linked data |
| `tei/` | TEI XML | Digital humanities |
| `txt/` | Plain text | Source documents |
| `uima_cas/` | UIMA CAS XMI | INCEpTION native |
| `webanno/` | WebAnno TSV 3.3 | Human-readable annotations |

### Top Documents by Annotation Density

| Document | Annotations |
|----------|-------------|
| `2.02 DE FORO COMPETENTI` | 3,943 |
| `1.02 DE CONSTITUTIONIBUS` | 3,080 |
| `1.33 DE MAIORITATE ET OBEDIENTIA` | 2,784 |

---

## Dependencies

```
dkpro-cassis     # UIMA CAS XMI reading/writing
scikit-learn     # ML utilities
sklearn-crfsuite # CRF implementation
python-docx      # DOCX processing
```

---

## Adaptation Notes for Stöckel Corpus

### What Can Be Reused

1. **CRF architecture** - The feature extraction and training pipeline
2. **BIOES tagging scheme** - Standard sequence labeling format
3. **INCEpTION workflow** - Annotation tool integration

### What Needs Modification

1. **TypeSystem** - Add new entity types:
   - `Biblical_Reference` - Scripture citations
   - `Contemporary_Reference` - Reformation-era sources

2. **Feature Engineering** - Consider adding:
   - Character n-grams for abbreviation patterns
   - Language detection (Latin vs. German)
   - Special handling for biblical book abbreviations

3. **Training Data** - Create new annotations in INCEpTION:
   - Export in same UIMA CAS XMI format
   - Maintain consistent annotation guidelines

---

## Recommended Testing Steps

1. **Verify environment:**
   ```bash
   python -c "import cassis; import sklearn_crfsuite; print('OK')"
   ```

2. **Test cas_to_bioes with sample data:**
   ```bash
   # After downloading Zenodo data
   python cas_to_bioes.py <zenodo_zip> <annotator_username>
   ```

3. **Run statistics on output:**
   ```bash
   python statistics.py annotations_bioes/
   ```

---

*Analysis conducted for ITSERR/RESILIENCE Fellowship pre-fellowship preparation.*

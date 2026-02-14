# Strategic Guide: Pre-Fellowship Preparation

**Author:** Michal Valčo
**Purpose:** Maximize the value of your ITSERR Transnational Access Fellowship by completing groundwork before arriving in Palermo.
**Related:** [Introduction 101](introduction-101.md) | [GNORM Integration](architecture/gnorm-integration.md)

---

## Repository Development: Pre-Fellowship Actions

This section outlines concrete steps to advance the repository *before* your Palermo visit, maximizing the value of your on-site time.

---

### 1. Clone and Explore the GNORM Annotation Pipeline

The GNORM team has published their code openly. This is a rare opportunity to study a production-quality religious studies annotation system.

**GitHub Repository:**
```bash
git clone https://github.com/aesuli/CIC_annotation.git
cd CIC_annotation
```

**What You'll Find:**
- CRF training pipeline for legal reference annotation
- BILOU schema implementation
- Preprocessing scripts for the *Liber Extra* text format
- Evaluation code (token-and-blank model)

**Dataset (Zenodo):**
- DOI: 10.5281/zenodo.14381709
- Contains the full index of 41,784 annotated legal references
- Linkages to lemmas, chapters, titles, and book parts

**Immediate Actions:**
1. Clone the repository and review the code structure
2. Download the Zenodo dataset
3. Run the annotation pipeline on their test data
4. Document any setup issues for discussion with Arianna's team

---

### 2. Prepare Leonard Stöckel Test Corpus

Your Stöckel corpus represents a perfect pilot study opportunity. The key question: **Can GNORM's CRF approach generalize to 16th-century Protestant theological texts?**

#### Why Stöckel Is Ideal for This Test

1. **Dense Citation Networks:** The *Annotationes in Locos communes* (1561) contains extensive references to:
   - Patristic sources (Augustine, Jerome, Chrysostom)
   - Biblical citations
   - Classical authors (Cicero, Plato, Aristotle)
   - Contemporary Reformers (Luther, Melanchthon)

2. **Structural Similarity to GNORM's Corpus:** Medieval glosses and Reformation-era commentaries share:
   - Abbreviated citation formats
   - Marginal apparatus structures
   - Argumentative use of authorities (*allegationes* logic)

3. **Research Gap:** No automated annotation system exists for Reformation-era theological commentaries

#### Corpus Preparation Steps

**Step 1: Select Initial Test Texts**

From your existing digitized Stöckel materials:
- 2-3 chapters from *Annotationes* (ideally with dense citations)
- The *Catechesis* (1556) — simpler citation structure, good baseline
- Selected passages from *Postilla* (1598) — homiletical genre comparison

**Step 2: Create Digital Text Files**

The GNORM pipeline expects plain text input. The project includes a full OCR pipeline:
1. Extract text from PDF using `ocr_processor.py` (Tesseract with Latin language pack, `--format txt` or `--format both` for ALTO XML)
2. Optionally parse ALTO XML with `extract_alto.py` for per-word confidence scores
3. Normalize text with `normalize_text.py`: spelling variants, abbreviation expansion, long-s correction
4. Mark structural elements: chapter breaks, lemma boundaries, gloss markers
5. Save in UTF-8 plain text format

**Step 3: Define Annotation Schema**

Adapt GNORM's schema for theological texts:

| Entity Type | GNORM Equivalent | Stöckel Application |
|-------------|------------------|---------------------|
| Glossed lemma | `Lemma glossato` | Commented biblical/theological term |
| Legal reference | `Allegazione normativa` | Patristic/biblical citation |
| Title | `Titolo` | Work referenced (e.g., *De Civitate Dei*) |
| Chapter | `Capitolo` | Specific passage location |
| **NEW:** Biblical reference | — | Scripture citations |
| **NEW:** Contemporary reference | — | Reformation-era sources |

**Step 4: Create Manual Training Annotations**

Following the GNORM methodology (expert annotates 10% for training):
- Annotate 2-3 representative sections manually using INCEpTION
- Ensure coverage of different citation types
- Document annotation decisions for consistency

---

### 3. Adapt the CRF Pipeline

#### Modification Strategy

The GNORM pipeline can likely transfer with minimal changes:

**Low-Risk Adaptations:**
- Adjust character encoding for 16th-century Latin/German
- Modify context window parameters for different citation density
- Add features for biblical book abbreviations

**Medium-Risk Adaptations:**
- Train on mixed Latin-German text
- Handle embedded vernacular phrases
- Recognize non-standard abbreviation patterns

**High-Risk (Requires Expert Input):**
- Multi-language reference extraction
- Genre-specific reference formats (homiletical vs. commentary)
- Handling of uncertain/reconstructed passages

#### Suggested Experiment Plan

**Experiment 1: Direct Transfer**
- Run GNORM's trained model on Stöckel text
- Evaluate: What does it find? What does it miss?
- Hypothesis: Will identify some patristic citations but miss biblical references

**Experiment 2: Retrained CRF**
- Use your manual annotations to train a new CRF
- Compare: Simple vs. rich feature configuration
- Document performance vs. GNORM's Liber Extra baseline

**Experiment 3: Hybrid Approach**
- Combine GNORM's pre-trained features with domain-specific additions
- Test whether knowledge transfer from canon law helps

---

### 4. Documentation and Integration

#### Create a "Stöckel Annotation" Sub-Project

Proposed directory structure:
```
03_prototype/
├── tests/                     # 11 test suites (414 tests)
└── stockel_annotation/
    ├── README.md              # Project description
    ├── PROGRESS.md            # Detailed progress tracking (18/23 tasks, 78%)
    ├── data/
    │   ├── raw/               # Original PDF and OCR output
    │   ├── cleaned/           # Preprocessed plain text (12 files)
    │   ├── alto/              # ALTO XML output (per-page, with confidence)
    │   ├── normalized/        # Text after normalization pipeline (~18,900 words)
    │   └── annotations/       # INCEpTION exports
    ├── models/
    │   ├── gnorm_baseline/    # Reference model
    │   └── stockel_crf/       # Domain-adapted model
    ├── scripts/               # 6 scripts, 3,603 LOC
    │   ├── ocr_processor.py   # Tesseract OCR (txt, ALTO XML, or both)
    │   ├── extract_alto.py    # ALTO XML → plaintext + confidence
    │   ├── normalize_text.py  # Text normalization (abbreviations, long-s)
    │   ├── cas_to_bioes.py    # INCEpTION CAS XMI → BIOES sequences
    │   ├── zero_shot_crf_experiment.py  # Cross-domain CRF transfer
    │   └── build_corpus_json.py  # Corpus Browser data generator
    ├── tools/
    │   └── inception/         # INCEpTION setup and annotation config
    └── results/
        └── experiments.md     # Documented findings
```

#### Integration with Main Agent

Design question for Palermo: How should the agent interact with annotation results?

**Option A: Query Interface**
- Agent can search the citation index
- "Find all references to Augustine in chapter 3"

**Option B: Active Annotation**
- Agent triggers annotation on uploaded texts
- Returns structured results with epistemic labels

**Option C: Collaborative Refinement**
- Agent assists human in reviewing uncertain annotations
- Flags low-confidence predictions for expert review

---

### 5. Questions to Prepare for Arianna's Team

**Technical Questions:**
1. What preprocessing challenges did you encounter with the *Liber Extra* text?
2. How did you handle ambiguous or incomplete references?
3. What features were most predictive in the CRF model?
4. Have you considered extending to non-legal religious texts?

**Methodological Questions:**
1. How do you validate annotation quality beyond accuracy metrics?
2. What's your approach to handling inter-annotator disagreement?
3. How do you balance automation with scholarly judgment?

**Integration Questions:**
1. Is there an API endpoint for GNORM's annotation service?
2. What data formats does GNORM accept/return?
3. How could external projects contribute to the T-ReS toolkit?

**Stöckel-Specific Questions:**
1. Would the team be interested in a Reformation-era test case?
2. What resources could support a pilot study?
3. Could this become a formal collaboration or publication?

---

### 6. Pre-Fellowship Deliverables Checklist

**Before February 10, 2026:**

- [ ] Clone GNORM repository and run test annotation
- [ ] Download Zenodo dataset and examine structure
- [ ] Select 2-3 Stöckel texts for pilot study
- [ ] Create cleaned digital versions
- [ ] Begin manual annotation in INCEpTION (minimum 100 references)
- [ ] Document annotation schema decisions
- [ ] Prepare technical questions document
- [ ] Draft email to Arianna outlining pilot study proposal
- [ ] Set up local development environment matching GNORM requirements

**During Fellowship (Palermo):**

- [ ] Review pilot study results with WP3 team
- [ ] Refine annotation schema based on feedback
- [ ] Train domain-adapted CRF model
- [ ] Evaluate performance and document findings
- [ ] Discuss integration architecture with GNORM team
- [ ] Plan joint publication or follow-up collaboration

**After Fellowship:**

- [ ] Complete Stöckel annotation pilot
- [ ] Publish code and results openly
- [ ] Submit blog post to ITSERR website
- [ ] Present at faculty seminar (Comenius University)
- [ ] Prepare conference submission (DH2026 or similar)
- [ ] Explore ELTF Observer status with RESILIENCE

---

### 7. Creative Extensions to Explore

#### A. Multi-Corpus Reference Network

Combine GNORM's canon law citations with Stöckel's theological citations to create a cross-domain reference network:
- How do Protestant reformers engage the same authorities as medieval canonists?
- Visualization of shared vs. distinct citation practices

#### B. Temporal Citation Analysis

Track how citation patterns evolve:
- Early Stöckel (1540s school regulations) vs. late Stöckel (1560s commentary)
- Compare with GNORM's chronological analysis of gloss development

#### C. Confessional Identity Through Citation

Use citation networks as markers of confessional identity:
- Which authorities distinguish Lutheran from Catholic texts?
- Can citation patterns predict theological position?

#### D. Educational Digital Humanities Module

Create teaching materials showing:
- How AI annotation works
- Comparison of manual vs. automatic methods
- Hands-on exercises with GNORM tools
- Ethical considerations in AI-assisted scholarship

---

### 8. Resource Links

**GNORM/ITSERR:**
- Project website: https://www.itserr.it/
- GitHub repository: https://github.com/aesuli/CIC_annotation
- Zenodo dataset: DOI 10.5281/zenodo.14381709
- CEUR paper: https://ceur-ws.org/Vol-3937/short6.pdf
- Digital Decretals source text: https://www.digitaldecretals.com/

**Annotation Tools:**
- INCEpTION: https://inception-project.github.io/
- CRFsuite documentation: https://www.chokkan.org/software/crfsuite/

**Your Stöckel Resources:**
- Existing digitized texts (check 04 Projekty/2021 KEGA Stockel)
- Published monograph materials
- Bibliographic databases for primary sources

**Training Events:**
- ITSERR Summer School (September 2025 — past event, materials may be available)
- "AI for Religious Studies" workshop at University of Palermo (check ITSERR website for upcoming dates)

---

*This guide integrates information from the COMPREHENSIVE_GUIDE_TO_GNORM.md, Andrea Esuli et al.'s "Automatic Annotation of Legal References" (IRCDL 2025), and the ITSERR Project Instructions and Strategy document.*

*Last updated: February 13, 2026*
*Part of the ITSERR Transnational Access Fellowship project*

# Stöckel Corpus Preparation: Progress Tracker

**Purpose:** Track progress on pre-fellowship preparation for the Stöckel annotation pilot study
**Deadline:** February 10, 2026 (Fellowship start)
**Last Updated:** January 25, 2026

---

## Quick Status Dashboard

| Category | Progress | Deadline |
|----------|----------|----------|
| GNORM Environment | 2/4 tasks | Feb 9 |
| Text Selection & Preparation | 0/6 tasks | Feb 7 |
| Annotation Work | 0/4 tasks | Feb 9 |
| Documentation & Communication | 1/4 tasks | Feb 9 |
| **Overall** | **3/18 tasks** | **Feb 9** |

---

## Phase 1: GNORM Environment Setup

### 1.1 Clone and Explore GNORM Repository

- [x] **Clone repository**
  ```bash
  git clone https://github.com/aesuli/CIC_annotation.git
  ```
  - Date completed: Jan 25, 2026
  - Notes: Cloned to `gnorm_repo/` subdirectory

- [x] **Review code structure**
  - [x] Examine CRF training pipeline (`train_crfsuite.py`)
  - [x] Understand BIOES schema implementation (`cas_to_bioes.py`)
  - [x] Review preprocessing scripts for *Liber Extra*
  - [x] Examine evaluation code (`statistics.py`, `annotate_by_crfsuite.py`)
  - Date completed: Jan 25, 2026
  - Notes: Full analysis documented in `scripts/GNORM_PIPELINE_ANALYSIS.md`

- [ ] **Run test annotation on sample data**
  - [x] Follow installation instructions (dependencies installed)
  - [ ] Run pipeline on provided test data (requires Zenodo dataset)
  - [ ] Document any setup issues
  - Date completed: ___
  - Notes: Blocked on Zenodo dataset download

### 1.2 Download and Examine Zenodo Dataset

- [ ] **Download dataset**
  - DOI: 10.5281/zenodo.14381709
  - [ ] Download complete dataset (manual download required)
  - [ ] Verify file integrity
  - Date completed: ___
  - Size: ___ MB
  - **ACTION REQUIRED:** Visit https://zenodo.org/records/14381709 and download manually
  - Instructions: See `data/raw/ZENODO_DOWNLOAD_INSTRUCTIONS.md`

- [ ] **Examine dataset structure**
  - [x] Document expected file formats (from code analysis)
  - [x] Understand annotation schema (BIOES tagging, UIMA CAS XMI)
  - [ ] Note: 41,784 annotated legal references (verify after download)
  - [ ] Study linkages to lemmas, chapters, titles, book parts
  - Date completed: ___
  - Notes: Expected format documented in `scripts/GNORM_PIPELINE_ANALYSIS.md`

---

## Phase 2: Stöckel Text Selection & Preparation

### 2.1 Select Test Texts

- [ ] **Select 2-3 chapters from *Annotationes in Locos communes* (1561)**
  - Criteria: High citation density, representative content
  - Selected chapters:
    1. ___
    2. ___
    3. ___
  - Date completed: ___
  - Rationale: ___

- [ ] **Identify *Catechesis* (1556) sections**
  - Purpose: Simpler citation structure for baseline comparison
  - Selected sections: ___
  - Date completed: ___

- [ ] **Select *Postilla* (1598) passages (optional)**
  - Purpose: Homiletical genre comparison
  - Selected passages: ___
  - Date completed: ___

### 2.2 Create Digital Text Files

- [ ] **Digitize selected texts (if needed)**
  - [ ] OCR using Transkribus or ABBYY
  - [ ] Verify OCR accuracy
  - Source location: ___
  - Date completed: ___

- [ ] **Clean and normalize texts**
  - [ ] Normalize spelling variants
  - [ ] Expand abbreviations consistently
  - [ ] Document normalization decisions
  - Files saved to: `data/cleaned/`
  - Date completed: ___

- [ ] **Mark structural elements**
  - [ ] Chapter breaks
  - [ ] Lemma boundaries
  - [ ] Gloss markers
  - [ ] Save in UTF-8 plain text format
  - Date completed: ___

---

## Phase 3: Manual Annotation

### 3.1 Annotation Schema Definition

- [ ] **Document annotation schema decisions**
  - [ ] Define entity types (see README.md table)
  - [ ] Create annotation guidelines document
  - [ ] Define edge cases and ambiguities
  - [ ] Document differences from GNORM schema
  - Output file: `data/annotations/annotation_guidelines.md`
  - Date completed: ___

### 3.2 INCEpTION Setup

- [ ] **Install and configure INCEpTION**
  - [ ] Download INCEpTION
  - [ ] Create project for Stöckel corpus
  - [ ] Configure annotation layers
  - [ ] Import cleaned text files
  - Date completed: ___

### 3.3 Manual Annotation Work

- [ ] **Begin manual annotation (minimum 100 references)**
  - Target: 100+ annotated references
  - Current count: ___
  - [ ] Patristic citations (Augustine, Jerome, Chrysostom, etc.)
  - [ ] Biblical citations
  - [ ] Classical citations (Cicero, Plato, Aristotle)
  - [ ] Contemporary references (Luther, Melanchthon)
  - Date completed: ___
  - Notes on annotation challenges: ___

- [ ] **Export annotations**
  - [ ] Export from INCEpTION
  - [ ] Save to `data/annotations/`
  - [ ] Verify export format compatibility with GNORM pipeline
  - Date completed: ___

---

## Phase 4: Documentation & Communication

### 4.1 Technical Documentation

- [ ] **Prepare technical questions document**
  - See: `01_research/gnorm_briefing_questions.md`
  - [ ] Review and update questions based on code exploration
  - [ ] Add Stöckel-specific technical questions
  - Date completed: ___

### 4.2 Communication

- [ ] **Draft email to Arianna outlining pilot study proposal**
  - [ ] Explain Stöckel corpus selection rationale
  - [ ] Outline proposed collaboration
  - [ ] Attach sample annotated text
  - Email drafted: ___
  - Email sent: ___

### 4.3 Development Environment

- [x] **Set up local development environment**
  - [x] Python 3.11+ installed
  - [ ] Create virtual environment (recommended for isolation)
  - [x] Install GNORM dependencies (dkpro-cassis, scikit-learn, sklearn-crfsuite, python-docx)
  - [x] Install CRFsuite (via sklearn-crfsuite)
  - [x] Verify environment matches GNORM requirements
  - Date completed: Jan 25, 2026
  - Notes: Dependencies installed globally; recommend venv for production use

### 4.4 Initial Results Documentation

- [ ] **Create initial experiments.md**
  - Output file: `results/experiments.md`
  - [ ] Document baseline expectations
  - [ ] Set up evaluation metrics template
  - [ ] Define success criteria
  - Date completed: ___

---

## Weekly Check-In Log

### Week of January 27, 2026

**Focus:** ___

**Completed:**
-

**In Progress:**
-

**Blockers:**
-

**Next Week Priority:**
-

---

### Week of February 3, 2026

**Focus:** ___

**Completed:**
-

**In Progress:**
-

**Blockers:**
-

**Final Push Items:**
-

---

## Notes & Decisions Log

Use this section to record important decisions, insights, and issues encountered.

| Date | Topic | Decision/Note |
|------|-------|---------------|
| Jan 25, 2026 | Project initialization | Created tracking structure and directory layout |
| Jan 25, 2026 | GNORM cloned | Repository cloned to `gnorm_repo/` successfully |
| Jan 25, 2026 | Pipeline analysis | Full analysis documented in `scripts/GNORM_PIPELINE_ANALYSIS.md` |
| Jan 25, 2026 | BIOES vs BILOU | GNORM uses BIOES scheme (B/I/E/S/O), not BILOU |
| Jan 25, 2026 | Zenodo access | API not accessible; manual download required |
| Jan 25, 2026 | Dependencies | Installed: dkpro-cassis, scikit-learn, sklearn-crfsuite, python-docx |
| Jan 25, 2026 | Entity types | GNORM supports: AN (allegation), LEMMA, CHAPTER, TITLE |

---

## Resources Quick Links

- **GNORM Repository:** https://github.com/aesuli/CIC_annotation
- **Zenodo Dataset:** https://doi.org/10.5281/zenodo.14381709
- **INCEpTION:** https://inception-project.github.io/
- **CRFsuite Docs:** https://www.chokkan.org/software/crfsuite/
- **GNORM Paper (CEUR):** https://ceur-ws.org/Vol-3937/short6.pdf
- **Strategic Guide:** `docs/introduction-101-strategic.md`
- **GNORM Briefing Questions:** `01_research/gnorm_briefing_questions.md`

---

## Success Criteria (Pre-Fellowship)

Before arriving in Palermo on February 10, 2026, you should be able to:

- [ ] Run the GNORM pipeline on test data successfully
- [ ] Have 2-3 cleaned Stöckel texts ready in `data/cleaned/`
- [ ] Have at least 100 manually annotated references
- [ ] Articulate the annotation schema decisions clearly
- [ ] Have specific technical questions prepared for the WP3 team
- [ ] Have drafted the pilot study proposal email

---

*Track updates by editing this file and committing changes.*
*Related: [README.md](README.md) | [../README.md](../README.md)*

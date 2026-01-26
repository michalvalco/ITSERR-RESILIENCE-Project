# Stöckel Corpus Preparation: Progress Tracker

**Purpose:** Track progress on pre-fellowship preparation for the Stöckel annotation pilot study
**Deadline:** February 10, 2026 (Fellowship start)
**Last Updated:** January 26, 2026

---

## Quick Status Dashboard

| Category | Progress | Deadline |
|----------|----------|----------|
| GNORM Environment | 4/4 tasks | Feb 9 |
| Text Selection & Preparation | 2/6 tasks | Feb 7 |
| Annotation Work | 0/4 tasks | Feb 9 |
| Documentation & Communication | 4/4 tasks | Feb 9 |
| **Overall** | **10/18 tasks** | **Feb 9** |

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

- [x] **Run test annotation on sample data**
  - [x] Follow installation instructions (dependencies installed)
  - [x] Run pipeline on provided test data
  - [x] Document any setup issues
  - Date completed: Jan 25, 2026
  - Notes: Dataset verified; WebAnno TSV format analyzed

### 1.2 Download and Examine Zenodo Dataset

- [x] **Download dataset**
  - DOI: 10.5281/zenodo.14381709
  - [x] Download complete dataset
  - [x] Verify file integrity
  - Date completed: Jan 25, 2026
  - Size: ~170 MB (all formats)
  - Contents: 186 documents in 7 formats (conll, conllu, nif, tei, txt, uima_cas, webanno)

- [x] **Examine dataset structure**
  - [x] Document expected file formats (from code analysis)
  - [x] Understand annotation schema (WebAnno TSV 3.3, UIMA CAS XMI)
  - [x] Verified: 18,425 annotation tokens, 462 unique legal references (expert set)
  - [x] Study linkages to lemmas, chapters, titles, book parts
  - Date completed: Jan 25, 2026
  - Notes: Full analysis in `results/zenodo_dataset_analysis.md`

---

## Phase 2: Stöckel Text Selection & Preparation

### 2.1 Select Test Texts

- [x] **Select 2-3 chapters from *Annotationes in Locos communes* (1561)**
  - Criteria: High citation density, representative content
  - Selected chapters:
    1. *De Peccato Originis* (On Original Sin) — 40-60 est. citations
    2. *De Iustificatione* (On Justification) — 50-70 est. citations
    3. *De Lege et Evangelio* (On Law and Gospel) — 35-50 est. citations
  - Date completed: Jan 25, 2026
  - Rationale: See `CHAPTER_SELECTION.md` for full analysis

- [ ] **Identify *Catechesis* (1556) sections**
  - Purpose: Simpler citation structure for baseline comparison
  - Selected sections: ___
  - Date completed: ___

- [ ] **Select *Postilla* (1598) passages (optional)**
  - Purpose: Homiletical genre comparison
  - Selected passages: ___
  - Date completed: ___

### 2.2 Create Digital Text Files

- [ ] **Digitize selected texts (if needed)** — IN PROGRESS
  - [x] OCR processor script created (`scripts/ocr_processor.py`)
  - [x] Tesseract OCR with Latin language pack installed
  - [x] Initial OCR test: pages 1-5 extracted successfully
  - [ ] Full OCR extraction (pages 1-58)
  - Source: `data/raw/Annotationes Locorum Communium, 1561 - Stoeckel - first 58 pages.pdf`
  - Date completed: Jan 25, 2026 (initial test); Jan 26, 2026 (tools verified)

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

- [x] **Prepare technical questions document**
  - See: `01_research/gnorm_briefing_questions.md`
  - [x] Review and update questions based on code exploration
  - [x] Add Stöckel-specific technical questions (sections 11-16)
  - Date completed: Jan 25, 2026
  - Notes: Added 6 Stöckel-specific question sections covering citation formats, biblical references, patristic abbreviations, mixed language handling, training data requirements, and structural differences

### 4.2 Communication

- [x] **Draft email to Arianna outlining pilot study proposal**
  - [x] Explain Stöckel corpus selection rationale
  - [x] Outline proposed collaboration
  - [ ] Attach sample annotated text (pending: text digitization)
  - Email drafted: Jan 25, 2026
  - Email sent: ___
  - Draft location: `05_admin/correspondence/2026-01-25_arianna_pilot_study_draft.md`

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

- [x] **Create initial experiments.md**
  - Output file: `results/experiments.md`
  - [x] Document baseline expectations (GNORM metrics from Zenodo)
  - [x] Set up evaluation metrics template
  - [x] Define success criteria (minimum, target, stretch goals)
  - Date completed: Jan 25, 2026

---

## Weekly Check-In Log

### Week of January 27, 2026

**Focus:** Text Digitization & OCR Setup

**Completed:**
- Selected 3 chapters from *Annotationes* for pilot study (CHAPTER_SELECTION.md)
- Added Stöckel-specific technical questions to briefing document (6 new sections)
- Drafted email to Arianna with pilot study proposal
- Created `ocr_processor.py` script with Tesseract Latin OCR
- Completed initial OCR test (pages 1-5)
- Addressed Copilot code review feedback (10 suggestions implemented)
- Fixed GNORM briefing questions section numbering (sections now consecutive 1-16)

**In Progress:**
- Full OCR extraction (58 pages, processing in 5-page chunks)
- Text cleaning and normalization

**Blockers:**
- INCEpTION installation (requires local setup time)

**Next Week Priority:**
- Complete full OCR extraction for all 58 pages
- Clean and normalize extracted text
- Install INCEpTION and configure annotation project
- Begin manual annotation (target: 50+ references by Feb 3)

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
| Jan 25, 2026 | Zenodo downloaded | 186 docs complete corpus; 39 docs expert annotations |
| Jan 25, 2026 | Format discovery | WebAnno TSV 3.3 format with `Allegazione normativa` labels |
| Jan 25, 2026 | Statistics | 18,425 annotation tokens; 462 unique references (expert set) |
| Jan 25, 2026 | Best reference doc | `2.02 DE FORO COMPETENTI` has 3,943 annotations (highest density) |
| Jan 25, 2026 | experiments.md | Added baseline expectations, metrics template, and success criteria |
| Jan 25, 2026 | Chapter selection | Selected 3 chapters: De Peccato Originis, De Iustificatione, De Lege et Evangelio |
| Jan 25, 2026 | Selection rationale | High citation density (125-180 est.), diverse types (biblical, patristic, Reformation) |
| Jan 25, 2026 | Briefing questions | Added 6 Stöckel-specific question sections (11-16) to gnorm_briefing_questions.md |
| Jan 25, 2026 | Email draft | Pilot study proposal to Arianna drafted; awaiting review before sending |
| Jan 25, 2026 | OCR processor | Created `scripts/ocr_processor.py` with Tesseract Latin support |
| Jan 25, 2026 | OCR test | Initial test: pages 1-5 extracted to `data/cleaned/annotationes_pp1-5.txt` |
| Jan 26, 2026 | OCR tools verified | Tesseract 5.3.4 + Latin pack + pdf2image + pytesseract all working |
| Jan 26, 2026 | Copilot review | Addressed 10 code review suggestions for ocr_processor.py |

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

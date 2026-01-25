# Stöckel Corpus Preparation: Progress Tracker

**Purpose:** Track progress on pre-fellowship preparation for the Stöckel annotation pilot study
**Deadline:** February 10, 2026 (Fellowship start)
**Last Updated:** January 25, 2026

---

## Quick Status Dashboard

| Category | Progress | Deadline |
|----------|----------|----------|
| GNORM Environment | 0/4 tasks | Feb 9 |
| Text Selection & Preparation | 0/6 tasks | Feb 7 |
| Annotation Work | 0/4 tasks | Feb 9 |
| Documentation & Communication | 0/4 tasks | Feb 9 |
| **Overall** | **0/18 tasks** | **Feb 9** |

---

## Phase 1: GNORM Environment Setup

### 1.1 Clone and Explore GNORM Repository

- [ ] **Clone repository**
  ```bash
  git clone https://github.com/aesuli/CIC_annotation.git
  ```
  - Date completed: ___
  - Notes: ___

- [ ] **Review code structure**
  - [ ] Examine CRF training pipeline
  - [ ] Understand BILOU schema implementation
  - [ ] Review preprocessing scripts for *Liber Extra*
  - [ ] Examine evaluation code (token-and-blank model)
  - Date completed: ___
  - Notes: ___

- [ ] **Run test annotation on sample data**
  - [ ] Follow installation instructions
  - [ ] Run pipeline on provided test data
  - [ ] Document any setup issues
  - Date completed: ___
  - Notes: ___

### 1.2 Download and Examine Zenodo Dataset

- [ ] **Download dataset**
  - DOI: 10.5281/zenodo.14381709
  - [ ] Download complete dataset
  - [ ] Verify file integrity
  - Date completed: ___
  - Size: ___ MB

- [ ] **Examine dataset structure**
  - [ ] Document file formats
  - [ ] Understand annotation schema
  - [ ] Note: 41,784 annotated legal references
  - [ ] Study linkages to lemmas, chapters, titles, book parts
  - Date completed: ___
  - Notes: ___

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

- [ ] **Set up local development environment**
  - [ ] Python 3.11+ installed
  - [ ] Create virtual environment
  - [ ] Install GNORM dependencies
  - [ ] Install CRFsuite
  - [ ] Verify environment matches GNORM requirements
  - Date completed: ___
  - Notes: ___

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
| | | |
| | | |

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

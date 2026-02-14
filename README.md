<div align="center">

# ITSERR / RESILIENCE Project

### Ethically-Grounded AI Agents for Religious Studies Research

*From Personalist Anthropology to Technical Implementation*

[![License: MIT](https://img.shields.io/badge/Code-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Documentation](https://img.shields.io/badge/docs-MkDocs%20Material-blue.svg)](https://michalvalco.github.io/ITSERR-RESILIENCE-Project/)
[![Tests](https://img.shields.io/badge/tests-414%20passing-brightgreen.svg)](#test-coverage)
[![Python](https://img.shields.io/badge/python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Fellowship](https://img.shields.io/badge/ITSERR%20TNA-UniPa%202026-blueviolet.svg)](#at-a-glance)

---

**Adapting the GNORM/CIC annotation pipeline** — originally built for detecting legal citations in medieval Canon law — **to detect theological citations** (biblical, patristic, confessional) **in 16th--18th century religious texts from the Kingdom of Hungary** as a long-term goal, with the current pilot focusing on a 16th-century text by Leonard Stockel.

</div>

---

## At a Glance

| | |
|---|---|
| **Fellowship** | ITSERR Transnational Access (TNA), University of Palermo |
| **Period** | February 10--27, 2026 |
| **Fellow** | Prof. Michal Valco (Comenius University Bratislava, ELTF) |
| **Hosts** | Dr. Arianna Maria Pavone & Marcello Costa (UniPa Software Lab) |
| **Status** | Day 5 of 18 -- Pipeline documentation complete, working paper drafted |
| **Live Docs** | [michalvalco.github.io/ITSERR-RESILIENCE-Project](https://michalvalco.github.io/ITSERR-RESILIENCE-Project/) |

---

## What This Project Does

This project bridges **twenty years of theological hermeneutics** with **AI agent development** to create tools for religious studies that respect hermeneutical complexity. Conducted in collaboration with the University of Palermo's Software Lab and the GNORM project team, it delivers three interlocking contributions:

### 1. A Philosophical Framework

A **personalist anthropology** (Mounier, Buber, Wojtyla) grounded in hermeneutical theory (Gadamer, Ricoeur) that defines *how* AI should handle religious texts -- distinguishing what it can verify, what it can suggest, and what it must defer to human judgment.

### 2. A 7-Stage Technical Pipeline

A complete **GNORM adaptation workflow** for processing 16th-century Latin theological texts through OCR, normalization, annotation, CRF-based entity detection, and interactive visualization -- with 6 production scripts and 414 passing tests.

### 3. An Epistemic Classification System

A **tripartite indicator system** -- `FACTUAL`, `INTERPRETIVE`, `DEFERRED` -- that operates at every layer of the pipeline, from CRF confidence scores to the interactive Corpus Browser, ensuring researchers always know the reliability of what they see.

---

## The Pipeline: Seven Stages

The core technical contribution follows Marcello Costa's data processing framework (Fry 2007), adapted for theological text analysis. Full specification: [`01_research/workflow_diagram.md`](01_research/workflow_diagram.md)

```
  ACQUIRE        PARSE          FILTER         MINE          REPRESENT      REFINE       INTERACT
 --------      --------       --------      --------       ----------     --------     ----------
| DIKDA  | -> | OCR    | -> | Entity | -> | 6-Layer| -> | Corpus   | -> | Filter | -> | Omeka S |
| Images |    | + ALTO |    | Schema |    | Detect |    | Browser  |    | & Sort |    | + IIIF  |
 --------      --------       --------      --------       ----------     --------     ----------
  Stage 1       Stage 2        Stage 3       Stage 4        Stage 5       Stage 6       Stage 7
  ~4000 pg      6 scripts      7 types       CRF+Rules      Dashboard     By type       Web UI
```

### Stage 2: Parse -- The OCR Pipeline (Built and Tested)

Six production scripts process digitized pages into pipeline-ready annotated sequences:

| Script | LOC | Tests | Purpose |
|--------|----:|------:|---------|
| `ocr_processor.py` | 427 | 34 | Tesseract OCR with Latin support -> plaintext + ALTO XML |
| `extract_alto.py` | 681 | 55 | ALTO XML parser -> plaintext + per-word confidence CSV |
| `normalize_text.py` | 839 | 121 | Orthographic normalization + abbreviation expansion with provenance logging |
| `cas_to_bioes.py` | 593 | 48 | INCEpTION CAS XMI -> BIOES-tagged sequences (multi-entity-type) |
| `zero_shot_crf_experiment.py` | 590 | 56 | Cross-domain CRF transfer experiment |
| `build_corpus_json.py` | 473 | 21 | Corpus Browser data generator with detection provenance |
| **Total** | **3,603** | **335** | *+ 79 agent tests = 414 total* |

### Stage 4: Mine -- Six-Layer Detection

```
Layer 1: Rule-based regex (84 patterns for biblical, patristic, confessional refs)
Layer 2: Abbreviation dictionary (consumes expansion_log from Stage 2)
Layer 3: Trie matching + statistical gap prediction
Layer 4: CRF machine learning (trained on INCEpTION annotations)
Layer 5: Structural parsing (section headers, chapter markers)
Merge:   Priority L1 > L2 > L3 > L4 > L5, with post-processing
```

When multiple layers agree on a detection -> **FACTUAL**. When they disagree -> **DEFERRED** for human review.

### Stage 5: Represent -- Corpus Browser Prototype

An interactive three-column browser with dashboard, already detecting **31 references** across 5 types in the pilot corpus:

- 13 biblical citations | 11 classical references | 4 patristic references
- 2 confessional references | 1 reformation reference
- Each reference carries detection **provenance** (which method found it) and **epistemic classification**

---

## Epistemic Modesty Framework

The core philosophical innovation: AI must be transparent about the *kind* of knowledge it is producing.

| Indicator | When Applied | Examples |
|-----------|-------------|----------|
| **`[FACTUAL]`** | >=2 methods agree, or single method with high confidence (biblical >=0.85, confessional >=0.80) | Dates, verified citations, direct quotes |
| **`[INTERPRETIVE]`** | Single method, moderate confidence (0.70--0.85) | Suggested patterns, thematic connections |
| **`[DEFERRED]`** | Methods disagree, confidence <0.70, or requires theological judgment | Truth claims, contested passages, value judgments |

This maps onto five registers of religious text, from historical-factual ("Luther posted 95 Theses in 1517") through existential-transformative ("What does this mean for my faith?") -- with AI competence decreasing as the register deepens.

Full framework: [`01_research/epistemic_modesty_framework.md`](01_research/epistemic_modesty_framework.md)

---

## Repository Structure

```
ITSERR-RESILIENCE-Project/
|
|-- 01_research/                        # Research foundations
|   |-- workflow_diagram.md             # * 7-stage GNORM adaptation pipeline (main technical spec)
|   |-- workflow_diagram_explained.md   #   Plain-language annotated version
|   |-- epistemic_modesty_framework.md  # * Philosophical framework (FACTUAL/INTERPRETIVE/DEFERRED)
|   |-- pipeline_overview.mermaid       #   Visual pipeline diagram
|   |-- literature_notes/               #   Annotated bibliographies
|   +-- sources/                        #   Key reference materials + bibliography
|
|-- 02_writing/                         # Written deliverables
|   |-- working_paper/                  # * "Personalist Foundations..." (~16-17K words, 9 sections)
|   |   |-- tna_working_paper_draft.md  #   Full synthesis draft
|   |   |-- 00_abstract.md ... 06_conclusion.md
|   |   +-- bibliography_final.md       #   ~160-170 verified entries
|   +-- blog_post/                      #   ITSERR/RESILIENCE website content (March 2026)
|
|-- 03_prototype/                       # Implementation (414 tests passing)
|   |-- src/itserr_agent/               # * Python agent package
|   |   |-- core/                       #   ITSERRAgent orchestration + Pydantic config
|   |   |-- memory/                     #   ChromaDB narrative memory (3 streams)
|   |   |-- epistemic/                  #   Indicator classification system
|   |   |-- integrations/               #   GNORM CRF client
|   |   +-- tools/                      #   Human-centered tool registry
|   |-- tests/                          #   11 test suites
|   |-- architecture/                   #   Design documents (system, memory, tools, epistemic)
|   |-- stockel_annotation/             # * Stockel corpus pilot study
|   |   |-- scripts/                    #   6 pipeline scripts (3,603 LOC)
|   |   |-- data/                       #   raw/ -> cleaned/ -> alto/ -> normalized/ -> annotations/
|   |   |-- PROGRESS.md                 #   Definitive progress tracker (18/23 tasks, 78%)
|   |   +-- tools/inception/            #   INCEpTION annotation setup
|   +-- pyproject.toml                  #   Package config (hatchling build)
|
|-- docs/                               # MkDocs Material site (37 pages)
|   |-- prototype/                      # * Interactive Corpus Browser (HTML app)
|   |-- pipeline/                       #   OCR pipeline documentation (6 stages)
|   |-- concepts/                       #   Epistemic indicators, narrative memory, tool patterns
|   |-- architecture/                   #   System design, memory, GNORM integration
|   +-- research/                       #   Philosophical foundations
|
|-- 04_presentations/                   # Consortium presentation (Feb 25/27)
|-- 05_admin/                           # Administrative docs, correspondence, milestones
|-- TNA_FELLOWSHIP_HUB.md              # * Navigation & status center for the fellowship
+-- mkdocs.yml                          #   Documentation site configuration
```

Files marked with `*` are key entry points.

---

## Quick Start

### Run the AI Agent

```bash
cd 03_prototype
pip install -e ".[dev]"

# With API key (full agent mode)
export ITSERR_ANTHROPIC_API_KEY="your-key"
itserr-agent chat

# Without API key (guided demo walkthrough)
itserr-agent demo
```

### Run the OCR Pipeline

```bash
cd 03_prototype

# OCR a PDF with Latin language support
python stockel_annotation/scripts/ocr_processor.py input.pdf --format both --lang lat

# Parse ALTO XML to plaintext + confidence scores
python stockel_annotation/scripts/extract_alto.py data/alto/ --confidence

# Normalize and expand abbreviations
python stockel_annotation/scripts/normalize_text.py data/cleaned/ --output data/normalized/

# Generate Corpus Browser data
python stockel_annotation/scripts/build_corpus_json.py
```

### Run the Tests

```bash
cd 03_prototype
pip install -e ".[dev]"
pytest tests/ -v
# 414 tests passing across 11 suites
```

### View the Documentation

```bash
# From repository root
pip install -e "03_prototype/.[dev]"
mkdocs serve
# Open http://127.0.0.1:8000
```

Live site: [michalvalco.github.io/ITSERR-RESILIENCE-Project](https://michalvalco.github.io/ITSERR-RESILIENCE-Project/)

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent** | LangChain / LangGraph | Agent orchestration with human-in-the-loop |
| **Memory** | ChromaDB + Sentence Transformers | Semantic narrative memory (3 streams) |
| **Tools** | Model Context Protocol (MCP) | Transparent, confirmable tool integration |
| **OCR** | Tesseract + ALTO XML | Latin text extraction with confidence scoring |
| **NLP** | CRFsuite + sklearn-crfsuite | Sequence labeling for entity detection |
| **Annotation** | INCEpTION + dkpro-cassis | Manual annotation + CAS XMI processing |
| **Visualization** | Interactive HTML/JS | Corpus Browser with dashboard |
| **Documentation** | MkDocs Material | 37-page documentation site with GitHub Pages |
| **Platform** | Python 3.11+ | Package managed via hatchling, tested with pytest |

---

## AI Agent Architecture

The `itserr-agent` package implements three core innovations:

### Narrative Memory System

Three distinct memory streams with different retention characteristics, backed by ChromaDB:

| Stream | Purpose | Retention |
|--------|---------|-----------|
| **Conversation** | Recent exchanges and clarifications | High recency weight, summarized periodically |
| **Research** | Sources consulted and notes created | Long-term, high relevance weight |
| **Decision** | Methodological and interpretive choices | Preserved indefinitely |

### Epistemic Classification (Dual-Layer)

1. **LLM-level:** System prompt instructs the model to tag outputs with `[FACTUAL]`, `[INTERPRETIVE]`, or `[DEFERRED]`
2. **Classifier-level:** Rule-based validation ensures consistent tagging across all responses

### Human-Centered Tool Patterns

Tools are categorized by autonomy level -- the more consequential the action, the more control the researcher retains:

| Category | Behavior | Example |
|----------|----------|---------|
| **Read-Only** | Auto-execute | Memory retrieval, searches |
| **Note-Taking** | Optional confirmation | Creating notes, annotations |
| **Modification** | Requires explicit approval | File operations |
| **External** | Confirmation + first-time gate | GNORM API calls |

---

## Stockel Corpus Pilot Study

The pipeline is being tested on Leonard Stockel's *Annotationes in Locos communes* (1561) -- a 16th-century Latin theological commentary with dense citation networks.

**Why Stockel?**
- Dense citation networks (biblical, patristic, confessional references)
- Structural similarity to medieval glosses (the same pattern GNORM was built for)
- Research gap: no automated annotation system exists for Reformation-era commentaries

### Current Data

| Metric | Value |
|--------|-------|
| Normalized files | 12 (from 57 pages) |
| Total words processed | ~18,900 |
| OCR noise characters removed | 1,913 |
| Abbreviations expanded | 156 (17 pattern types) |
| Long-s corrections | 658 |
| References detected (Layer 1) | 31 across 5 types |
| Overall pilot progress | 18/23 tasks (78%) |

### Entity Types (Proposed Schema)

| Type | Example | Parallel in GNORM/CIC |
|------|---------|----------------------|
| Biblical_citation | Matt. 5,3--12 | Allegazione normativa |
| Patristic_reference | Aug. de civ. Dei XIV.28 | Allegazione normativa |
| Confessional_reference | CA Art. IV | -- (new) |
| Hymnological_reference | Cithara Sanctorum No. 42 | -- (new) |
| Cross_reference | vid. supra cap. III | -- (new) |
| Glossed_term | *iustitia originalis* | Lemma glossato |
| Section_header | CAPVT III | Capitolo / Titolo |

---

## Test Coverage

414 tests across 11 suites -- all passing:

| Suite | Tests | Coverage Area |
|-------|------:|---------------|
| Text Normalization | 121 | OCR noise, abbreviation expansion, long-s, structure, reference patterns |
| Zero-Shot CRF | 56 | Feature extraction, inference, confidence, XML tag stripping |
| ALTO XML Parser | 55 | Namespace detection, hyphenation, confidence scores, batch processing |
| CAS to BIOES | 48 | Multi-type support, entity labels, positional info, roundtrip |
| OCR Processor | 34 | Text/ALTO/both extraction, version guard, backward compatibility |
| Corpus Builder | 21 | JSON generation, detection patterns, epistemic classification |
| GNORM Client | 18 | API calls, error handling |
| Integration | 17 | End-to-end pipeline workflows |
| Memory Streams | 17 | Conversation, research, decision streams |
| Reflection | 14 | Summarization, memory updates |
| Epistemic | 13 | Classification logic, indicator tagging |

---

## Key Deliverables

| # | Deliverable | Status | Location |
|---|------------|--------|----------|
| 1 | **Working Paper** -- "Personalist Foundations for AI-Assisted Theological Research" (~16-17K words) | Integration pass complete | [`02_writing/working_paper/`](02_writing/working_paper/) |
| 2 | **7-Stage Workflow Diagram** -- GNORM adaptation for Stockel corpus | Complete, reviewed against code | [`01_research/workflow_diagram.md`](01_research/workflow_diagram.md) |
| 3 | **OCR Pipeline** -- 6 scripts, 3,603 LOC, 414 tests | Production-ready | [`03_prototype/stockel_annotation/scripts/`](03_prototype/stockel_annotation/scripts/) |
| 4 | **Corpus Browser** -- Interactive prototype with dashboard | Layer 1 complete | [`docs/prototype/`](docs/prototype/) |
| 5 | **Epistemic Modesty Framework** | Complete | [`01_research/epistemic_modesty_framework.md`](01_research/epistemic_modesty_framework.md) |
| 6 | **AI Agent Prototype** -- Narrative memory + epistemic classification + tool patterns | Functional | [`03_prototype/src/itserr_agent/`](03_prototype/src/itserr_agent/) |
| 7 | **Documentation Site** -- 37 MkDocs pages | Deployed | [Live Site](https://michalvalco.github.io/ITSERR-RESILIENCE-Project/) |
| 8 | **Consortium Presentation** | Scheduled Feb 25 | [`04_presentations/`](04_presentations/) |
| 9 | **Blog Post** | Skeleton ready, due March 2026 | [`02_writing/blog_post/`](02_writing/blog_post/) |

---

## Levels of AI Engagement in Religious Studies

A typology of how AI can engage with religious/theological texts, with increasing interpretive depth:

| Level | Name | AI Role | Epistemic Status |
|-------|------|---------|-----------------|
| 1 | **Information Retrieval** | Finding, counting, verifying | Primarily FACTUAL |
| 2 | **Structured Synthesis** | Organizing, pattern identification | FACTUAL + INTERPRETIVE |
| 3 | **Interpretive Assistance** | Suggesting connections, flagging tensions | Primarily INTERPRETIVE |
| 4 | **Collaborative Reasoning** | Dialogue-based exploration | INTERPRETIVE + DEFERRED |

The pipeline operates primarily at Levels 1--2. The AI agent extends into Level 3. Level 4 always requires a human researcher in the loop.

---

## Context: ITSERR & RESILIENCE

**ITSERR** (Italian Strengthening of the ESFRI RI RESILIENCE) supports the **RESILIENCE** research infrastructure -- *Religious Studies Infrastructure: tooLs, Innovation, Experts, coNnections and Centres in Europe*.

### Relevant Work Packages

| WP | Name | Connection to This Project |
|----|------|---------------------------|
| **WP3** | **T-ReS** | Direct collaboration -- GNORM team provides the base pipeline and CRF methodology |
| WP4 | DaMSym | Semantic textual analysis insights for entity classification |
| WP6 | YASMINE | Ethical guidelines for AI handling of religious content |
| WP7 | REVER | Hermeneutical traditions informing ML application design |
| WP8 | UbiQuity | Citation network analysis and cross-reference challenges |

---

## Related Projects

| Project | Link | Relationship |
|---------|------|-------------|
| **GNORM / CIC_annotation** | [github.com/aesuli/CIC_annotation](https://github.com/aesuli/CIC_annotation) | Source pipeline being adapted |
| **Digital Decretals** | [github.com/Digital-Decretals](https://github.com/Digital-Decretals) | Source text project for GNORM's original domain |
| **APVV-2026** | Private repository | 4-year grant project for Stockel corpus (broader scope) |
| **INCEpTION** | [inception-project.github.io](https://inception-project.github.io) | Annotation platform for training data |
| **GNORM Prototype** | [ariannapavone.com/gnorm](https://ariannapavone.com/gnorm/) | Arianna's GNORM visualization demo |

---

## Timeline

### Week 1 (Feb 10--16): Foundation

- Meet WP3 team, receive GNORM technical briefing
- Produce 7-stage workflow diagram from code inspection
- Build OCR pipeline (6 scripts, 3,603 LOC)
- Achieve 414 passing tests
- Complete working paper draft (~16-17K words)
- Documentation audit across all files

### Week 2 (Feb 17--23): Refinement

- Zero-shot CRF experiment on Stockel sample
- Entity schema validation with Palermo team
- Working paper revision pass
- Miro canvas population

### Week 3 (Feb 24--27): Delivery

- Consortium presentation (Feb 25)
- Final documentation and handoff
- Blog post draft

---

## License

| Component | License |
|-----------|---------|
| **Code** (scripts, agent, tests) | [MIT License](LICENSE) |
| **Documentation & Writing** (papers, docs, diagrams) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

---

## Author

**Prof. Michal Valco**
Comenius University Bratislava, Evangelical Lutheran Theological Faculty

-- with substantial help from **Claude Code**, who helped organize ideas and write code

## Acknowledgments

This research is supported by the **ITSERR Transnational Access Fellowship** program, hosted by the **University of Palermo**. Special thanks to:

- **Dr. Arianna Maria Pavone** and the GNORM project team (WP3)
- **Marcello Costa** for the pipeline framework and methodology guidance
- **Prof. Andrea Ferrara** and the UniPa Software Lab
- The **RESILIENCE** research infrastructure consortium

---

<div align="center">

*Part of the [RESILIENCE](https://www.intl.unipd.it/resilience) Research Infrastructure*

**[Documentation](https://michalvalco.github.io/ITSERR-RESILIENCE-Project/)** · **[Workflow Diagram](01_research/workflow_diagram.md)** · **[Working Paper](02_writing/working_paper/tna_working_paper_draft.md)** · **[Corpus Browser](docs/prototype/)**

</div>

# 03_prototype

AI agent prototype development for the ITSERR/RESILIENCE project.

## Structure

```
03_prototype/
├── architecture/         # Design documents
├── code_notes/           # Technical decisions log
├── src/                  # Python agent source code (itserr_agent package)
├── tests/                # Test suites (376 tests across 10 files)
└── stockel_annotation/   # Stöckel corpus pilot study (GNORM adaptation)
```

## Core Innovations

### 1. Narrative Memory System
Contextual continuity across research sessions, preserving the hermeneutical journey.

- Stores conversation history with semantic indexing
- Retrieves relevant past context for new queries
- Maintains researcher's interpretive trajectory

### 2. Epistemic Modesty Indicators
Clear differentiation between response types:

| Indicator | Meaning | Example |
|-----------|---------|---------|
| `[FACTUAL]` | Verifiable information | Dates, citations, definitions |
| `[INTERPRETIVE]` | AI-assisted analysis | Pattern identification, connections |
| `[DEFERRED]` | Requires human judgment | Theological claims, value judgments |

### 3. Human-Centered Tool-Calling Patterns
Ensuring researcher maintains agency and control:

- Transparent tool invocation (user sees what's being called)
- Confirmation for significant actions
- Easy override/correction mechanisms

## Stöckel Annotation Pilot Study

Testing GNORM's CRF-based annotation approach on 16th-century Reformation theological texts.

**Directory:** `stockel_annotation/`

| Component | Purpose |
|-----------|---------|
| `data/raw/` | Original PDF and OCR output from Stöckel texts |
| `data/cleaned/` | Preprocessed, normalized plain text |
| `data/alto/` | ALTO XML output from Tesseract (per-page, with confidence) |
| `data/annotations/` | INCEpTION exports (manual annotations) |
| `scripts/ocr_processor.py` | Tesseract OCR extraction (txt, ALTO XML, or both) |
| `scripts/extract_alto.py` | ALTO XML parser: plaintext + confidence scores |
| `scripts/normalize_text.py` | Text normalization (abbreviations, long-s, structure) |
| `scripts/cas_to_bioes.py` | INCEpTION CAS XMI export → BIOES token tags for CRF |
| `scripts/zero_shot_crf_experiment.py` | Cross-domain transfer experiment (GNORM → Stöckel) |
| `scripts/build_corpus_json.py` | Generates `corpus.json` for the Corpus Browser prototype |
| `models/` | Trained CRF models (when available) |
| `results/experiments.md` | Documented findings |

**Progress Tracking:** See `stockel_annotation/PROGRESS.md`

---

## Technical Stack

- **Python 3.11+**
- **LangChain / LangGraph** — Agent orchestration
- **Model Context Protocol (MCP)** — Tool integration
- **ChromaDB** — Vector database for semantic memory
- **CRFsuite** — Sequence labeling for Stöckel annotation
- **Tesseract OCR** — PDF text extraction with Latin language support
- **pytesseract** — Python wrapper for Tesseract (ALTO XML via `image_to_alto_xml`)

## Architecture Documents (`architecture/`)

| Document | Purpose |
|----------|---------|
| `system_design.md` | Overall architecture overview |
| `memory_architecture.md` | Narrative memory system design |
| `epistemic_indicators.md` | Modesty indicator implementation |
| `tool_patterns.md` | Human-centered tool-calling design |

## Code Notes (`code_notes/`)

Technical decision log documenting:

- Design choices and rationale
- Philosophical annotations mapping principles to code
- Integration notes with ITSERR/GNORM tools
- Lessons learned and iterations

## Development Timeline

| Week | Development Goals |
|------|-------------------|
| Week 1 | Environment setup, review GNORM patterns |
| Week 2 | Implement narrative memory architecture |
| Week 3 | Complete prototype, document codebase |

## Related Resources

- [GNORM Annotation Code](https://github.com/aesuli/CIC_annotation)
- [GNORM Zenodo Dataset](https://doi.org/10.5281/zenodo.14381709)
- [INCEpTION Annotation Tool](https://inception-project.github.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
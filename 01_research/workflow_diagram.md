# Workflow Diagram: GNORM Adaptation for Slovak Religious Heritage

**Prepared for:** Marcello Costa, Arianna Pavone, and the Palermo team  
**Framework:** Based on Marcello's data processing pipeline (Fry 2007)  
**Date:** 12 February 2026 (created) | 13 February 2026 (revised)  
**Status:** Working draft — revised after Feb 12 meeting and code analysis. Ready for Miro transfer and collaborative refinement.

---

## Project in One Sentence

We want to adapt the GNORM/CIC_annotation pipeline — originally built for detecting legal citations in medieval Canon law — to detect theological citations (biblical, patristic, confessional) in 16th-18th century religious texts from the Kingdom of Hungary - with the focus on present-day Slovakia (Upper Hungary) - (German, Latin, old Czech), starting with the works of Leonard Stöckel (Latin and German).

---

## Target Users and Value Chain

### Who Generates Value

| Actor | Contribution |
|-------|-------------|
| **Church historians** (Valčo, Hanus, Kowalská) | Domain expertise: identifying citation patterns, validating annotations, building abbreviation dictionaries, creating training data in INCEpTION |
| **Library scientists** (Kollárová, SNK/Glončák) | Source materials: providing digitised images, ALTO XML metadata, bibliographic records |
| **GNORM/WP3 team** (Pavone, Ravasco, Imperia, Esuli, Puccetti) | Technical methodology: the annotation pipeline, CRF models, architectural expertise |
| **Annotators** (Hanus, Kollárová + doctoral student) | Manual annotation in INCEpTION to create training data |

### Who Consumes Value

| User | What They Need | Format |
|------|---------------|--------|
| **Reformation scholars** | Searchable citation networks — "Which texts cite Romans 3:28?" "What patristic sources does Stöckel rely on most?" | Web interface (Omeka S), exportable datasets |
| **Historical linguists** | Annotated corpus with orthographic variants identified | TEI XML, CSV exports |
| **Slovak National Library** | Enriched metadata for DIKDA items; integration with Kramerius 7 | Dublin Core, MARC21-compatible outputs |
| **RESILIENCE network** | Demonstrated methodology for expanding GNORM to new domains | Documentation, reproducible pipeline, trained models |
| **APVV evaluators** | Evidence that the methodology works | Published results, pilot study data |

### Domain Context

16th–18th century Protestant theology and other religious texts in the Kingdom of Hungary. Texts are primarily in Latin with German and early Czech or Slovak passages. The reference apparatus includes biblical citations, Church Fathers, Reformation confessional documents, and cross-references to other theological works. These citation patterns are **structurally similar** to the legal citations GNORM was built for — abbreviated references pointing to canonical source texts — but use entirely different abbreviation conventions and reference hierarchies.

---

## The Seven Stages

### STAGE 1: ACQUIRE

**Question:** How do we get the source texts into the pipeline?

```
[Physical books in Lyceum Libraries]
        ↓ (already done by SNK/DIKDA)
[TIFF/PNG/JPG/JPEG2000 master images]
        ↓
[Available in DIKDA digital repository]
```

**Current state:**
- ~3,000–4,000 pages of Stöckel's works already digitised (TIFF images)
- Additional Reformation-era prints available at Kežmarok and Prešov Lyceum Libraries
- DIKDA (Slovak National Library) holds digitised collections accessible online
- Total target: 8,000–10,000 pages over 4-year project period

**Formats:** TIFF, PNG, JPG, JPEG2000 (images); ALTO XML (OCR metadata where available)

**Tools:** DIKDA portal, direct library access for materials not yet in DIKDA

**What we do NOT do:** We do not digitise. We work with existing digitised materials only.

**Open questions for Palermo team:**
- Does GNORM assume any particular image quality or resolution threshold?
- Any standard acquisition checklist beyond this workflow? (This document serves as our working checklist.)

---

### STAGE 2: PARSE

**Question:** How do we convert images into machine-readable text?

```
[TIFF/JPEG2000 images]
        ↓ (OCR)
[ALTO XML with word-level data]
        ↓ (extraction — TO BE BUILT)
[Clean plaintext]
        ↓ (existing CIC_annotation script)
[BIOES-tagged sequences for pipeline input]
```

**Current state:**
- Some materials have existing ABBYY FineReader OCR output (ALTO XML)
- Other materials may need fresh OCR processing
- **Basic OCR/PDF text extraction is available** via Tesseract + Poppler (installed in prototype environment) — sufficient for initial text extraction from PDFs and images
- **The ALTO XML → pipeline-format extraction step does not exist yet** — CIC_annotation uses `split_docx.py` for DOCX input; a script to parse ALTO XML structure (word-level bounding boxes, confidence scores) into one-token-per-line plaintext for the BIOES pipeline is still needed
- No testing has been done on how OCR errors affect GNORM annotation accuracy

**Formats:**
- Input: TIFF/JPEG2000
- Intermediate: ALTO XML (from ABBYY), potentially Transkribus PAGE XML (for Fraktur)
- Target: Clean plaintext → BIOES-tagged sequences

**Tools:**
- ABBYY FineReader (SNK standard) — works well on Antiqua (Latin script)
- Transkribus or Kraken — needed for Fraktur (Gothic script) materials
- Tesseract OCR + Poppler (installed in prototype) — available for basic PDF/image text extraction
- Custom script needed: ALTO XML → pipeline-format extractor (preserving page/line structure, confidence scores)

**Key technical challenges:**
- Historical orthographic variation: ſ/s, ij/j, cz/č, w/v, ß/ss
- Decision needed: normalise orthography *before* or *after* CRF processing?
- OCR error rates on 16th-century print are unknown — empirical testing required
- Multilingual documents (Latin/German/Slovak switches within paragraphs)

**Open questions for Palermo team:**
- Should we preserve ALTO word-level confidence scores for downstream filtering?
- Recommendations for handling OCR noise — post-processing rules or noisy training data?
- Marcello suggested Transkribus for handwriting recognition — to be explored for marginalia if encountered

---

### STAGE 3: FILTER

**Question:** What categories and entity types do we define for annotation?

```
[Clean plaintext]
        ↓ (entity type schema applied)
[Annotated text with typed entities]
```

**Current state:**
- CIC_annotation uses 4 entity types: Allegazione normativa, Lemma glossato, Capitolo, Titolo
- We propose 7 entity types for Protestant theological texts (see below)
- No annotation protocol drafted yet — need to define what counts as each type

**Proposed entity type schema:**

| Entity Type | Description | Example | CIC Parallel |
|-------------|-------------|---------|-------------|
| Biblical_citation | Direct reference to Scripture | *Matt. 5,3–12* | Allegazione normativa |
| Patristic_reference | Reference to Church Fathers | *Aug. de civ. Dei XIV.28* | Allegazione normativa |
| Confessional_reference | Reference to Reformation documents | *CA Art. IV* | Allegazione normativa |
| Hymnological_reference | Reference to hymns/liturgical texts | *Cithara Sanctorum No. 42* (Tranovský, 1636 — Czech text; tests pipeline on non-Latin scripts) | (new) |
| Cross_reference | Internal reference to other works | *vid. supra cap. III* | (new) |
| Glossed_term | Theological term being defined | *iustificatio, fides* | Lemma glossato |
| Section_header | Structural element | *Caput III: De fide* | Titolo / Capitolo |

**Key decisions needed:**
- Can the CRF handle all 7 types simultaneously, or do we train separate models?
- What counts as a biblical "citation" vs. an "allusion" vs. a "paraphrase"?
- How do we handle composite references (*Matt. 5,3 et Luc. 6,20*)?
- Annotation boundary: the reference string only, or reference + framing context?

**Open questions for Palermo team:**
- Arianna: what was your experience with multiple entity types in the CRF?
- What is the minimum inter-annotator agreement needed before training?

---

### STAGE 4: MINE

**Question:** How do we detect patterns — specifically, how do we run the GNORM pipeline?

```
[BIOES-tagged plaintext]
        ↓ Layer 1: Rule-based detection (regex patterns for Protestant citations)
        ↓ Layer 2: Abbreviation dictionary lookup (theological abbreviations)
        ↓ Layer 3: Trie matching + statistical gap prediction
        ↓ Layer 4: CRF machine learning (trained on our annotated data)
        ↓ Layer 5: Structural parsing (section headers, chapter markers)
        ↓ Merge with priority + post-processing
[Annotated output with source tracking]
```

**Current state:**
- CIC_annotation pipeline is installed and runnable (`CIC_annotation` repo)
- Pipeline is trained on Canon law — needs domain-specific adaptation at every layer
- Zero-shot test on Stöckel sample not yet conducted (priority deliverable)
- The pipeline's `mark_source` mechanism provides provenance for each annotation

**What needs adaptation per layer:**

| Layer | Current (CIC) | Needed (Protestant) | Effort |
|-------|---------------|---------------------|--------|
| Rules | Legal citation regex patterns | Biblical/patristic/confessional regex patterns | Medium — requires domain knowledge |
| Abbreviations | Canon law abbreviation dictionary | Protestant theological abbreviation dictionary | Medium — we can compile this |
| Match model | Trained on CIC patterns | Retrain on Protestant patterns | Low — once training data exists |
| CRF | Trained on CIC annotations | Retrain; possibly add character-level features | Medium-High — core technical work |
| Structural | CIC document structure | 16th-c. printed book structure (chapters, marginalia) | Medium |
| Post-processing | "ff." correction rule | Domain-specific error corrections (TBD from error analysis) | Low — driven by empirical findings |

**The roundtrip:**

```
INCEpTION (manual annotation) → export ZIP (UIMA CAS XMI)
    → cas_to_bioes.py → BIOES plaintext
    → pipeline processing (6 layers)
    → bioes_to_cas.py → UIMA CAS XMI
    → import back to INCEpTION for expert review
```

**Epistemological classification** (connecting to TNA's philosophical framework):

| Classification | Criteria | Action |
|----------------|----------|--------|
| FACTUAL | ≥2 pipeline methods agree AND CRF confidence ≥0.85 | Accept; include in public dataset |
| INTERPRETIVE | CRF alone, or confidence 0.70–0.85 | Flag for expert review |
| DEFERRED | Methods disagree, or confidence <0.70, or requires theological judgment | Route to human annotator |

**Design note:** This dual-path approach — method consensus across pipeline layers *plus* CRF marginal probabilities within the ML layer — is more robust than either mechanism alone, and represents a methodological extension beyond the original CIC_annotation design.

**Open questions for Palermo team:**
- Zero-shot test results will determine where to focus adaptation effort
- Code analysis confirms the layered architecture is domain-agnostic (CRF is entity-type agnostic, merge logic is format-agnostic) — but would value Arianna's confirmation and any caveats from experience
- Character-level features for orthographic variation — worth adding?

---

### STAGE 5: REPRESENT

**Question:** How do we initially visualise what the pipeline has found?

```
[Annotated output]
        ↓
[Citation index / cross-reference database]
        ↓
[Basic visualisations: frequency tables, citation networks]
```

**Current state:**
- CIC_annotation produces a `LegalReferences.csv` cross-reference index (on Zenodo)
- GNORM has a 3D visualisation component (mentioned in ITSERR docs, not yet seen)
- Arianna demonstrated the GNORM prototype web interface at ariannapavone.com/gnorm/
- We have no visualisation infrastructure set up yet

**Planned initial representations:**
- Citation frequency tables (which sources does Stöckel cite most?)
- Co-citation analysis (which sources appear together?)
- Simple network graphs (D3.js or similar)

**Formats:** CSV/JSON for data; HTML/JS for web visualisation

**Open questions for Palermo team:**
- What does the 3D visualisation component actually visualise?
- What input format does it require?
- Is it available for us to test?

---

### STAGE 6: REFINE

**Question:** How do we customise the visualisation for our research questions?

**Planned refinements:**
- Filter by citation type (biblical vs. patristic vs. confessional)
- Chronological analysis across Stöckel's works (does his citation pattern change?)
- Geographical filtering (if corpus expands to multiple authors/regions)
- Confidence-based filtering (show only FACTUAL annotations, or include INTERPRETIVE)

**This stage is downstream — not a priority during the fellowship.** But the data structures designed in Stages 3–5 must support these refinements.

---

### STAGE 7: INTERACT

**Question:** What is the final product? Who uses it and how?

```
[Enriched, annotated corpus]
        ↓
[Omeka S platform] ← researchers browse, search, explore
        ↓
[IIIF integration] ← link annotations back to source images
        ↓
[Exportable datasets] ← CSV, TEI XML, Dublin Core for reuse
```

**Planned platform:** Omeka S (open source, IIIF-native, supports Dublin Core metadata)

**User interactions:**
- "Show me all texts that cite Romans 3:28" → filtered search results
- "Which patristic sources does Stöckel rely on?" → frequency analysis
- "Compare citation patterns between Stöckel and his contemporaries" → cross-corpus analysis
- View annotations overlaid on original page images (IIIF)

**Integration with Slovak infrastructure:**
- Output compatible with SNK's DIKDA/Kramerius 7
- Metadata exportable in Dublin Core and MARC21
- Alignment with FAIR data principles and 5-Star Open Data

**This stage is mostly WP4 of the APVV grant — long-term, not fellowship scope.**

---

## Data Flow Summary

```
DIKDA / Lyceum Libraries
    │ (TIFF/JPEG2000 images)
    ▼
OCR Processing (ABBYY / Transkribus)
    │ (ALTO XML)
    ▼
Text Extraction (Tesseract/Poppler available; ALTO XML → pipeline format TO BE BUILT)
    │ (clean plaintext)
    ▼
INCEpTION (manual annotation for training data)
    │ (UIMA CAS XMI)
    ▼
CIC_annotation Pipeline (adapted)
    │ Rules → Abbreviations → Match → CRF → Structure → Merge
    │ (annotated output with source tracking)
    ▼
Epistemological Classification
    │ FACTUAL / INTERPRETIVE / DEFERRED
    ▼
Cross-Reference Index + Citation Database
    │ (CSV / JSON)
    ▼
Omeka S Platform
    │ Web interface, IIIF, exportable datasets
    ▼
Researchers, Libraries, RESILIENCE Network
```

---

## Current Materials Status

| Item | Status | Format |
|------|--------|--------|
| Stöckel sample texts (20–30pp) | 🔧 TO PREPARE — Tesseract/Poppler available for extraction; need to run on sample pages | Plaintext (.txt) |
| Preliminary abbreviation list | 🔧 TO COMPILE from Stöckel corpus conventions | CSV or Markdown table |
| This workflow document | ✅ DRAFT — ready for Miro transfer | Markdown |
| CIC_annotation code analysis | ✅ COMPLETE (567-line Deep Dive report) | Markdown |
| Pipeline technical reference | ✅ COMPLETE (quick-lookup reference card, 230 lines) | Markdown |
| Entity type schema proposal | ✅ DRAFT — in Stage 3 above; needs validation against samples | Table |
| Zero-shot test | 🔧 NOT STARTED — blocked on sample text preparation | — |

---

## Interoperability Commitments (per Marcello's guidance)

| Principle | Implementation |
|-----------|---------------|
| No proprietary formats for working documents | Markdown, CSV, JSON, XML only |
| Version control | Git (this repo) |
| FAIR data principles | Metadata, persistent identifiers, open formats |
| Reproducibility | Pipeline scripts, configuration files, documented parameters |

---

## References

- Esuli, A., Imperia, R., & Puccetti, G. (2025). Automatic Annotation of Legal References in the *Liber Extra*. CEUR-WS Vol. 3937 (IRCDL 2025).
- Puccetti, G., Imperia, R., & Esuli, A. (2024). GNORM overview. *ERCIM News* 141.
- Fry, B. (2007). *Visualizing Data*. O'Reilly. [Chapter 1 — framework for data processing stages]
- GO FAIR Initiative. (2022). FAIR Principles. https://www.go-fair.org/fair-principles/
- 5-Star Open Data. https://5stardata.info/en/

---

*This document maps to Marcello's Miro canvas framework. Next step: transfer the seven stages and data flow to the canvas for collaborative refinement.*

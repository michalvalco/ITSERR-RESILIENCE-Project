# Workflow Diagram: GNORM Adaptation for Slovak Religious Heritage
# 🎓 Annotated Edition — with plain-language explanations

**Original prepared for:** Marcello Costa, Arianna Pavone, and the Palermo team  
**This version:** Annotated for non-technical readers (colleagues, students, grant evaluators, librarians)  
**Framework:** Based on Marcello's data processing pipeline (Fry 2007)  
**Date:** 13 February 2026 (created) | 14 February 2026 (updated: test counts, Stage 5 Visualization, materials status)

> 🎓 **What is this document?**
>
> This is an annotated copy of our project's main technical workflow. The original text is preserved in full. After each section, you'll find a plain-language explanation marked with 🎓 that translates the technical language into everyday terms. Think of it as a guided tour through the project — the technical blueprint is here if you need precision, and the explanations are here if you need clarity.

---

## Project in One Sentence

We want to adapt the GNORM/CIC_annotation pipeline — originally built for detecting legal citations in medieval Canon law — to detect theological citations (biblical, patristic, confessional) in 16th-18th century religious texts from the Kingdom of Hungary - with the focus on present-day Slovakia (Upper Hungary) - (German, Latin, old Czech), starting with the works of Leonard Stöckel (Latin and German).

> 🎓 **In even simpler terms:**
>
> Italian researchers built a computer tool that can automatically find and tag legal references inside medieval law books. We want to take that same tool and teach it to find *theological* references instead — Bible verses, Church Father quotations, Reformation documents — inside the writings of Leonard Stöckel, a 16th-century Slovak Protestant theologian. It's like taking a search engine trained to find case law and retraining it to find Scripture citations.

---

## Target Users and Value Chain

### Who Generates Value

| Actor | Contribution |
|-------|-------------|
| **Church historians** (Valčo, Hanus, Kowalská) | Domain expertise: identifying citation patterns, validating annotations, building abbreviation dictionaries, creating training data in INCEpTION |
| **Library scientists** (Kollárová, SNK/Glončák) | Source materials: providing digitised images, ALTO XML metadata, bibliographic records |
| **GNORM/WP3 team** (Pavone, Ravasco, Imperia, Esuli, Puccetti) | Technical methodology: the annotation pipeline, CRF models, architectural expertise |
| **Annotators** (Hanus, Kollárová + doctoral student) | Manual annotation in INCEpTION to create training data |

> 🎓 **Who does the work?**
>
> Four groups of people contribute to making this happen:
> - **Historians** who actually understand the old texts and can tell the computer what a Bible reference looks like vs. a reference to a Church Father vs. a reference to a hymnal.
> - **Librarians** at the Slovak National Library who already photographed the old books and can provide us with digital images.
> - **The Italian tech team** who built the original tool and know how it works under the hood.
> - **Annotators** — people who sit down with the text on screen and manually highlight references so the computer can learn from their examples. This is like creating an answer key for the machine.

### Who Consumes Value

| User | What They Need | Format |
|------|---------------|--------|
| **Reformation scholars** | Searchable citation networks — "Which texts cite Romans 3:28?" "What patristic sources does Stöckel rely on most?" | Web interface (Omeka S), exportable datasets |
| **Historical linguists** | Annotated corpus with orthographic variants identified | TEI XML, CSV exports |
| **Slovak National Library** | Enriched metadata for DIKDA items; integration with Kramerius 7 | Dublin Core, MARC21-compatible outputs |
| **RESILIENCE network** | Demonstrated methodology for expanding GNORM to new domains | Documentation, reproducible pipeline, trained models |
| **APVV evaluators** | Evidence that the methodology works | Published results, pilot study data |

> 🎓 **Who benefits from it?**
>
> Once the tool works, several groups of people get something valuable:
> - **Scholars** can search the texts in ways that were never possible before — for instance, instantly finding every place Stöckel quotes the Apostle Paul, or mapping which Church Fathers he relies on most.
> - **Linguists** get a carefully labelled dataset showing how Latin (and German, and Czech) was actually written in the 1500s — spelling variants and all.
> - **The Slovak National Library** gets enriched catalogue records for their digital collections.
> - **The European research network** (RESILIENCE) gets a proven example of how to adapt these tools for new kinds of texts.
> - **Grant evaluators** get evidence that the method actually works.

### Domain Context

16th–18th century Protestant theology and other religious texts in the Kingdom of Hungary. Texts are primarily in Latin with German and early Czech or Slovak passages. The reference apparatus includes biblical citations, Church Fathers, Reformation confessional documents, and cross-references to other theological works. These citation patterns are **structurally similar** to the legal citations GNORM was built for — abbreviated references pointing to canonical source texts — but use entirely different abbreviation conventions and reference hierarchies.

> 🎓 **Why does this adaptation make sense?**
>
> Here's the key insight: a legal citation like "*Decretales, Lib. II, Tit. 3, Cap. 5*" and a theological citation like "*Matt. 5,3–12*" look very different on the surface, but they work the same way structurally. Both are shorthand codes that point to a specific passage in a well-known source text. The original tool learned to spot one kind of shorthand; we need to teach it the other kind. The grammar of referencing is similar — only the vocabulary changes.

---

## The Seven Stages

> 🎓 **Why seven stages?**
>
> Our Italian colleague Marcello organised the whole workflow into seven steps, following a standard framework from data science (Fry 2007). Every data project — whether you're analysing sports statistics or medieval manuscripts — follows roughly this path: get the data, clean it up, define your categories, run your analysis, show the results, refine them, and put them into a form people can actually use. The stages below walk through each step as it applies to our project.

---

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

> 🎓 **Stage 1 in plain language: Getting the photographs**
>
> Before you can do anything with old books on a computer, someone needs to photograph every page. The good news is that the Slovak National Library has already done this for thousands of pages of Stöckel's works. These high-resolution photographs are stored in their digital repository called DIKDA. Our job starts *after* the photography — we don't scan books ourselves.
>
> Think of it like this: the library took the photos; we develop them into something a computer can read.

---

### STAGE 2: PARSE

**Question:** How do we convert images into machine-readable text?

```
[TIFF/JPEG2000 images or PDFs]
        ↓ (OCR)
[ocr_processor.py --format both]
        ↓                    ↓
[ALTO XML]          [Clean plaintext]
[data/alto/*.xml]   [data/cleaned/*.txt]
        ↓
[extract_alto.py → confidence scores.csv]
        ↓
[normalize_text.py]
        ↓
[data/normalized/*.txt → Pre-annotated plaintext with XML-like tags]
        ↓
[Import to INCEpTION for manual annotation / training data creation]
        ↓
[cas_to_bioes.py → BIOES-tagged sequences for pipeline input]
```

**Current state:**
- ✅ `ocr_processor.py` supports `--format {txt,alto,both}` — Tesseract produces ALTO XML and/or plaintext in one step
- ✅ `extract_alto.py` parses ALTO XML, extracts text + confidence scores (per-word `WC` attribute) into companion CSV
- ✅ `normalize_text.py` handles orthographic normalization (long-s, ligatures, v/u confusion) and abbreviation expansion with provenance logging
- ✅ `cas_to_bioes.py` converts INCEpTION CAS XMI exports → BIOES-tagged sequences for CRF training (multi-type support)
- ✅ `zero_shot_crf_experiment.py` provides cross-domain CRF transfer experiment framework
- ✅ `build_corpus_json.py` generates Corpus Browser data with detection provenance and epistemic classification
- ✅ 414 tests passing across 11 suites (see `PROGRESS.md` for authoritative count per suite)
- Some DIKDA materials have existing ABBYY FineReader OCR output (ALTO XML) — `extract_alto.py` handles these directly without re-running OCR
- No testing has been done yet on how OCR error rates on 16th-century print affect downstream GNORM annotation accuracy
- ⚠️ **Important:** `normalize_text.py` outputs pre-annotated plaintext (XML-like `<ref>` and `<chapter>` tags), NOT BIOES sequences. The BIOES conversion happens later: normalized text → INCEpTION (human annotation) → `cas_to_bioes.py` → pipeline. This human annotation loop is the bridge between Stage 2 (Parse) and Stage 4 (Mine).

**Formats:**
- Input: TIFF/JPEG2000
- Intermediate: ALTO XML (from ABBYY), potentially Transkribus PAGE XML (for Fraktur)
- Target: Pre-annotated plaintext with XML-like tags (`<ref type="biblical">`, `<chapter>`, etc.) for INCEpTION import. BIOES tagging happens downstream via `cas_to_bioes.py` after human annotation in INCEpTION.

**Tools:**
- ABBYY FineReader (SNK standard) — works well on Antiqua (Latin script); DIKDA materials may already have ALTO XML from this
- Transkribus or Kraken — needed for Fraktur (Gothic script) materials
- ✅ Tesseract OCR + Poppler — installed; `ocr_processor.py` handles PDF/image → ALTO XML + plaintext
- ✅ `extract_alto.py` — parses ALTO XML (both Tesseract and ABBYY output) into plaintext + confidence CSV
- ✅ `normalize_text.py` — orthographic normalization for historical text

**Key technical challenges:**
- Historical orthographic variation: ſ/s, ij/j, cz/č, w/v, ß/ss
- Decision needed: normalise orthography *before* or *after* CRF processing?
- OCR error rates on 16th-century print are unknown — empirical testing required
- Multilingual documents (Latin/German/Slovak switches within paragraphs)

> 🎓 **Stage 2 in plain language: Teaching the computer to read old print**
>
> A photograph of a page is just a picture — the computer doesn't know there are words on it. **OCR** (Optical Character Recognition) is the technology that looks at the image and converts the shapes of letters into actual text that a computer can search, copy, and analyse. It's the same technology your phone uses when you scan a receipt.
>
> The catch is that 16th-century books look very different from modern ones. The letter "s" was often printed as "ſ" (a tall, f-like shape), abbreviations were everywhere, and some books used Gothic-style lettering (called **Fraktur**) that's hard even for specialised software. So after the OCR runs, we have to **clean up the text**: fix the ſ→s confusion, expand abbreviations like "Xpi" back to "Christi," and mark structural elements like chapter headings.
>
> The output at this stage is a reasonably clean text with preliminary markings — like a rough draft with highlighted notes saying "this looks like a Bible reference" or "this seems to be a chapter heading." But these markings are *suggestions*, not final labels. They're meant to help the human experts in the next stage, not to replace them.
>
> **The crucial thing to understand:** this stage does NOT produce the machine-ready labelled data the pipeline needs. That comes later, after human experts review and correct the text. There's a deliberate human checkpoint between "cleaned-up text" and "data the pipeline can learn from."

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

> 🎓 **Stage 3 in plain language: Deciding what to look for**
>
> Before the computer can find anything, we have to tell it exactly *what kinds of things* to look for. This is like giving a student a highlighter and saying: "Mark every Bible verse in yellow, every Church Father quote in green, every reference to the Augsburg Confession in blue..."
>
> The original Italian tool was trained to find one main type of reference: legal citations in Canon law. We need to define **seven types** for our theological texts:
>
> 1. **Bible references** — "Matt. 5,3–12" (the Gospel of Matthew, chapter 5, verses 3 through 12)
> 2. **Church Father references** — "Aug. de civ. Dei XIV.28" (Augustine's *City of God*, Book 14, Chapter 28)
> 3. **Confessional references** — "CA Art. IV" (the Augsburg Confession, Article 4)
> 4. **Hymnal references** — "Cithara Sanctorum No. 42" (a specific hymn in the Tranovský hymnal)
> 5. **Cross-references** — "vid. supra cap. III" ("see above, chapter 3" — pointing to another part of the same book)
> 6. **Theological terms being defined** — when Stöckel pauses to explain what *iustificatio* (justification) means
> 7. **Section headers** — chapter titles like "Caput III: De fide" (Chapter 3: On Faith)
>
> This is also the stage where **humans sit down with the text** in a specialised annotation tool called **INCEpTION** and manually mark up a sample of pages. They highlight each reference, assign it a type, and that hand-labelled data becomes the "answer key" the computer will learn from. This is the most labour-intensive part of the whole project — and the most important, because the quality of everything downstream depends on the quality of these human decisions.

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

> 🎓 **Stage 4 in plain language: The six-layer detection engine**
>
> This is the heart of the project — where the computer actually finds the references. But here's the surprise: it's not just one program doing the finding. It's **six different methods** running one after another, each catching things the others might miss. Think of it like six detectives working the same case, each with a different speciality:
>
> 1. **The Rule Follower** — knows that "Matt. 5,3" always means a Bible reference because it matches a predictable pattern (a book abbreviation, a period, a number, a comma, another number). Fast and precise, but only catches references that follow the expected format exactly.
>
> 2. **The Dictionary Expert** — has a list of every known abbreviation ("Aug." = Augustine, "CA" = Confessio Augustana, etc.) and flags them wherever they appear. Only as good as the dictionary we give it.
>
> 3. **The Pattern Matcher** — remembers patterns it has seen before in the training data and looks for similar ones. Also uses statistics to fill in small gaps (if words 1, 2, and 4 of a reference are found, it guesses word 3 probably belongs too).
>
> 4. **The Machine Learner (CRF)** — the most sophisticated method. A statistical model that has been *trained* on the hand-labelled examples from Stage 3. It looks at each word in context (the six words before it and the six words after it) and estimates the probability that this word is part of a reference. This is the layer that achieves the famous 97.8% accuracy on the original legal texts.
>
> 5. **The Structural Parser** — finds chapter headings, section titles, and other organisational elements based on formatting patterns.
>
> 6. **The Merger** — takes all the results from layers 1–5 and combines them. When multiple methods agree, we're more confident. When they disagree, we're more cautious. Each annotation gets a label saying *which method found it* — so a human reviewer can always see where a finding came from.
>
> **The honesty system.** After the pipeline runs, every annotation gets classified into one of three honesty levels:
> - **FACTUAL** — multiple methods agree AND the machine is very confident. We trust this and publish it.
> - **INTERPRETIVE** — only one method found it, or the confidence is moderate. We flag this for a human expert to check.
> - **DEFERRED** — the methods disagree, the confidence is low, or the question requires theological judgment that no machine should make. We hand this to a human annotator.
>
> This honesty system is something we're adding to the original Italian design. It's one of our project's intellectual contributions: the idea that a computer tool should be transparent about *how sure it is* and *how it knows what it knows.*
>
> **The roundtrip.** After the pipeline runs, its results go back into the annotation tool (INCEpTION) for human experts to review. They correct mistakes, the corrected data feeds back into training, and the pipeline gets better over time. It's a feedback loop, not a one-shot process.

---

### STAGE 5: REPRESENT

**Question:** How do we initially visualise what the pipeline has found?

```
                 CURRENT PROTOTYPE PATH          FUTURE FULL-PIPELINE PATH
                 ─────────────────────          ─────────────────────────
[data/normalized/*.txt]              [Annotated output (from Stage 4 layers)]
  (Stage 2 output)                      (BIOES + mark_source provenance)
        ↓                                        ↓
        └──────────┐               ┌─────────────┘
                   ▼               ▼
            [build_corpus_json.py]
              ↓ (converts → structured JSON with
              ↓  detection provenance and consensus tracking)
            [docs/prototype/data/corpus.json]
              ↓
            [Corpus Browser — docs/prototype/index.html]
              ↓ (interactive web-based exploration)
            [Citation index / cross-reference database]
              ↓
            [Basic visualisations: frequency tables, citation networks]
```

> **Note:** The current prototype reads directly from Stage 2 normalized text and applies its own rule-based detection. When the full CIC_annotation pipeline (Stage 4) is operational, `build_corpus_json.py` will consume its annotated output instead — the `crf_entities` parameter is already implemented for this.

**Current state:**
- ✅ **`build_corpus_json.py`** bridges the gap between the normalization pipeline output and the web prototype. It reads normalized text files from `data/normalized/`, applies enhanced rule-based reference detection (82 patterns: 58 biblical, 18 patristic/classical, 4 reformation, 2 confessional), and produces `docs/prototype/data/corpus.json`
- ✅ **Corpus Browser** (`docs/prototype/index.html`) provides an interactive three-column interface with dashboard, full-text search, entity/epistemic filtering, reference highlighting, and contextual detail panels
- ✅ **Epistemic classification** is applied at build time: each reference is tagged `FACTUAL`, `INTERPRETIVE`, or `DEFERRED` based on pattern quality and detection method(s)
- ✅ **Detection provenance** is tracked per reference: every annotation records which method(s) detected it (currently rule-based; CRF when integrated)
- CIC_annotation produces a `LegalReferences.csv` cross-reference index (on Zenodo)
- GNORM has a 3D visualisation component (mentioned in ITSERR docs, not yet seen)
- Arianna demonstrated the GNORM prototype web interface at ariannapavone.com/gnorm/

**Planned representations (beyond Corpus Browser):**
- Citation frequency tables (which sources does Stöckel cite most?)
- Co-citation analysis (which sources appear together?)
- Simple network graphs (D3.js or similar)

**Formats:** CSV/JSON for data; HTML/JS for web visualisation

> 🎓 **Stage 5 in plain language: Making the results visible**
>
> Once the pipeline has found all the references, we need to display them in a way humans can actually understand and explore. Raw data in a spreadsheet isn't very illuminating.
>
> We've built a **Corpus Browser** — an interactive web application where you can:
>
> - **See a dashboard** with statistics: how many references of each type, which chapters are densest, overall confidence levels
> - **Search the full text** and filter by entity type (biblical, patristic, confessional, etc.) or by epistemic status (FACTUAL, INTERPRETIVE, DEFERRED)
> - **Click on any reference** to see its details: what it is, how it was detected, how confident the system is
>
> Beyond the Corpus Browser, we plan:
> - **Frequency tables** — "Stöckel cites Romans 45 times, the Psalms 38 times, Augustine 27 times..."
> - **Network graphs** — visual maps showing which sources are cited together
> - **A searchable database** — so a scholar can type "Romans 3:28" and instantly see every passage
>
> The Italian team also has a 3D visualisation tool that we haven't explored yet.

---

### STAGE 6: REFINE

**Question:** How do we customise the visualisation for our research questions?

**Planned refinements:**
- Filter by citation type (biblical vs. patristic vs. confessional)
- Chronological analysis across Stöckel's works (does his citation pattern change?)
- Geographical filtering (if corpus expands to multiple authors/regions)
- Confidence-based filtering (show only FACTUAL annotations, or include INTERPRETIVE)

**This stage is downstream — not a priority during the fellowship.** But the data structures designed in Stages 3–5 must support these refinements.

> 🎓 **Stage 6 in plain language: Asking better questions**
>
> Once the basic visualisations work, scholars start asking more sophisticated questions: "Did Stöckel's reliance on Augustine change over his career?" "Do the early works cite different confessional documents than the later ones?" "If I only look at the high-confidence annotations, does the pattern change?"
>
> This stage is about giving researchers the ability to filter, slice, and re-examine the data from different angles. We're not building this yet — it's future work — but we're designing the earlier stages so these questions will be answerable later.

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

> 🎓 **Stage 7 in plain language: The finished product**
>
> The end goal is a **website** where researchers can browse Stöckel's works, see the original page images side by side with the computer-generated annotations, search for specific references, and download the data for their own research. Think of it as a specialised digital library — not just scanned pages, but pages that have been *read* and *understood* by the computer, with every Bible verse, every Church Father quotation, and every confessional reference highlighted and catalogued.
>
> The platform we plan to use (Omeka S) is designed for exactly this kind of cultural heritage presentation. It connects to a standard called **IIIF** ("Triple-I-F") that lets you link annotations directly to specific regions of page images — so you can click on a highlighted reference and see it in context on the original printed page.
>
> All the data will be freely available in standard formats, so other researchers can download it, remix it, and build on it. That's not just good practice — it's a requirement of our European funding.

---

## Data Flow Summary

```
DIKDA / Lyceum Libraries
    │ (TIFF/JPEG2000 images, PDFs)
    ▼
OCR Processing — ocr_processor.py --format both
    │ (ALTO XML + clean plaintext)          ✅ BUILT
    ▼
Confidence Extraction — extract_alto.py
    │ (confidence scores CSV)               ✅ BUILT
    ▼
Normalization — normalize_text.py
    │ (normalized plaintext + expansion_log) ✅ BUILT
    ▼
INCEpTION (manual annotation for training data)
    │ (UIMA CAS XMI)
    ▼
CIC_annotation Pipeline (adapted)
    │ Parallel: Rules · Abbreviations (← expansion_log) · Match · CRF · Structure
    │ → Merge (first-method-wins) → annotated output with source tracking
    ▼
Epistemological Classification
    │ FACTUAL / INTERPRETIVE / DEFERRED
    ▼
build_corpus_json.py (Stage 5 bridge)                 ✅ BUILT
    │ (normalized text → structured JSON with
    │  detection provenance and consensus tracking)
    ▼
Corpus Browser — docs/prototype/index.html             ✅ BUILT
    │ (interactive exploration with epistemic filters)
    ▼
Cross-Reference Index + Citation Database
    │ (CSV / JSON)
    ▼
Omeka S Platform
    │ Web interface, IIIF, exportable datasets
    ▼
Researchers, Libraries, RESILIENCE Network
```

> 🎓 **The whole thing in one story:**
>
> Old books sit in Slovak libraries → they've already been photographed → a computer reads the photographs and turns them into text → we clean up the text and fix old spelling → human experts sit down and manually highlight references in a sample of pages → those highlighted samples become the "answer key" → the six-layer pipeline learns from the answer key and processes all the remaining pages → each annotation gets an honesty label (sure / less sure / ask a human) → the results get organised into a Corpus Browser and searchable databases → scholars explore them on a website.
>
> That's it. Everything else is details about *how* each step works. But this is the arc.

---

## Current Materials Status

| Item | Status | Format |
|------|--------|--------|
| Stöckel sample texts (57pp) | ✅ COMPLETE — 12 normalized files in `data/normalized/`, ~18,900 words | Plaintext (.txt) |
| Preliminary abbreviation list | 🔧 PARTIALLY DONE — `normalize_text.py` contains 17 abbreviation patterns with `expansion_log` provenance. Broader dictionary still needed | Python dict + CSV or Markdown table |
| This workflow document | ✅ DRAFT — ready for Miro transfer | Markdown |
| CIC_annotation code analysis | ✅ COMPLETE (567-line Deep Dive report) | Markdown |
| Pipeline technical reference | ✅ COMPLETE (quick-lookup reference card, 230 lines) | Markdown |
| Entity type schema proposal | ✅ DRAFT — in Stage 3 above; needs validation against samples | Table |
| Zero-shot test script | ✅ READY — `zero_shot_crf_experiment.py` with 56 tests; awaiting CRF model | Python |
| Corpus Browser (prototype) | ✅ LIVE — `docs/prototype/index.html` with dashboard, search, consensus visualization | HTML/JS |
| JSON build bridge | ✅ BUILT — `build_corpus_json.py` converts pipeline → `corpus.json` with multi-method support | Python |

> 🎓 **Where are we right now?**
>
> The tools for reading and cleaning the text (Stages 1–2) are built and tested — 57 pages of Stöckel's *Annotationes* have been processed into 12 normalized text files. The category definitions (Stage 3) are drafted but need validation against real samples. The pipeline itself (Stage 4) is installed but trained on the wrong domain — it knows Canon law, not Protestant theology. A **zero-shot test script** is ready to run once the CRF model is available — feeding Stöckel's text through the existing Canon law pipeline *without any retraining* to see what happens. Meanwhile, the **Corpus Browser** (Stage 5) is already live, showing 31 detected references across 5 entity types using rule-based detection.

---

## Interoperability Commitments (per Marcello's guidance)

| Principle | Implementation |
|-----------|---------------|
| No proprietary formats for working documents | Markdown, CSV, JSON, XML only |
| Version control | Git (this repo) |
| FAIR data principles | Metadata, persistent identifiers, open formats |
| Reproducibility | Pipeline scripts, configuration files, documented parameters |

> 🎓 **What does "interoperability" mean here?**
>
> We've committed to using only open, standard file formats — no Microsoft Word documents or proprietary databases that lock people out. Everything is stored in formats that any researcher, anywhere, with free software, can open and use. We track every change using Git (a version control system that records the full history of who changed what and when). And we follow international principles called **FAIR** — data should be **F**indable, **A**ccessible, **I**nteroperable, and **R**eusable. In practice, this means someone ten years from now should be able to download our data and pipeline, understand what we did, and reproduce our results.

---

## References

- Esuli, A., Imperia, R., & Puccetti, G. (2025). Automatic Annotation of Legal References in the *Liber Extra*. CEUR-WS Vol. 3937 (IRCDL 2025).
- Puccetti, G., Imperia, R., & Esuli, A. (2024). GNORM overview. *ERCIM News* 141.
- Fry, B. (2007). *Visualizing Data*. O'Reilly. [Chapter 1 — framework for data processing stages]
- GO FAIR Initiative. (2022). FAIR Principles. https://www.go-fair.org/fair-principles/
- 5-Star Open Data. https://5stardata.info/en/

---

*Original document maps to Marcello's Miro canvas framework. This annotated edition created February 13, 2026, for non-technical readers.*

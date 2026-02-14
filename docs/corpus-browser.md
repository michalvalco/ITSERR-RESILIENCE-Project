# Corpus Browser Prototype

!!! info "Interactive Prototype"
    This page links to the **Stöckel Corpus Browser** — a standalone web application for browsing annotated 16th-century theological texts.

## Launch the Prototype

<div style="margin: 24px 0; padding: 20px; background: linear-gradient(135deg, #e8eaf6, #e3f2fd); border-radius: 8px; border: 1px solid #c5cae9;">
  <h3 style="margin-top: 0; color: #3f51b5;">Stöckel Corpus Browser</h3>
  <p>Browse Leonard Stöckel's <em>Annotationes in Locos communes</em> (1561) with rule-based entity annotations.</p>
  <p><a href="../prototype/" style="display: inline-block; padding: 8px 20px; background: #3f51b5; color: white; border-radius: 4px; text-decoration: none; font-weight: 500;">Open Corpus Browser &rarr;</a></p>
</div>

## What This Prototype Demonstrates

This is a **Layer 1 prototype** — the first stage of the GNORM adaptation pipeline for Protestant theological texts:

| Feature | Description |
|---------|-------------|
| **Interactive dashboard** | Stat cards, reference type bar chart, and chapter reference density heatmap on the welcome screen |
| **Three-column layout** | Text in the center, chapter navigation on the left, collapsible detail panel on the right |
| **Hierarchical navigation** | Browse by chapter (*locus*): title page, PRAEFATIO, DE DEO, DE TRINITATE, etc. (10 chapters) |
| **Rule-based entity detection** | 31 references across 5 types with OCR-variant pattern matching |
| **Epistemic indicators** | FACTUAL / INTERPRETIVE confidence levels on each detected reference |
| **Full-text search** | Search across the entire corpus with result highlighting and right-panel detail view |
| **Entity type filtering** | Toggle visibility of different reference types |
| **Reference detail panel** | Click any reference to see context, metadata, and related references in the right panel |

### Detection Statistics

| Entity Type | Count | Examples |
|-------------|-------|----------|
| Biblical | 13 | Psalm, Rom., Matth., Gen., Ioann. |
| Classical | 11 | Stoicorum, Epicureorum, Aristotle |
| Patristic | 4 | Augustini (incl. OCR variant Auguflini), Ambrosij |
| Confessional | 2 | in Symbolo Niceno, in Symbolo Athanasij |
| Reformation | 1 | Melanchthonis |
| **Total** | **31** | |

## Pipeline Stage

This prototype implements **Stage 5 (REPRESENT)** and **Stage 7 (INTERACT)** of the [workflow diagram](https://github.com/michalvalco/ITSERR-RESILIENCE-Project/blob/main/01_research/workflow_diagram.md), using output from Stage 4, Layer 1 (rule-based detection).

```
Stage 1: ACQUIRE    ✅  (DIKDA/Lyceum sources)
Stage 2: PARSE      ✅  (OCR → ALTO → normalized text)
Stage 3: FILTER     ✅  (Entity type schema defined)
Stage 4: MINE       ⚡  Layer 1 only (rule-based detection)
Stage 5: REPRESENT  ⚡  This prototype
Stage 6: REFINE     📋  Planned (filtering by type, confidence)
Stage 7: INTERACT   ⚡  This prototype
```

## Technical Details

- **Pure HTML/CSS/JS** — no build step, no framework dependencies, zero external libraries
- **Client-side rendering** — all data loaded from a single `corpus.json` file
- **CSS-only visualizations** — dashboard charts use CSS custom properties and flexbox (no D3/Chart.js)
- **OCR-variant patterns** — regex accounts for 16th-century long-s OCR artifacts (e.g., `Auguflini` → Augustini, `fymbolo` → symbolo)
- **Data generation** — `build_corpus_json.py` parses normalized text files with enhanced regex patterns
- **Keyboard accessible** — heatmap rows, search results, and panel items support keyboard navigation
- **XSS-safe** — all dynamic content escaped before innerHTML insertion
- **Hosted on GitHub Pages** — alongside the MkDocs documentation

## Next Steps

1. **Manual annotation in INCEpTION** — create training data for the CRF model
2. **CRF training** — adapt the GNORM CRF pipeline for Protestant theological texts
3. **Enhanced detection** — integrate CRF predictions into the corpus browser
4. **Citation network visualization** — D3.js graphs showing citation relationships

*Last updated: February 14, 2026*

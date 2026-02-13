# Corpus Browser Prototype

!!! info "Interactive Prototype"
    This page links to the **Stöckel Corpus Browser** — a standalone web application for browsing annotated 16th-century theological texts.

## Launch the Prototype

<div style="margin: 24px 0; padding: 20px; background: linear-gradient(135deg, #e8eaf6, #e3f2fd); border-radius: 8px; border: 1px solid #c5cae9;">
  <h3 style="margin-top: 0; color: #3f51b5;">Stöckel Corpus Browser</h3>
  <p>Browse Leonard Stöckel's <em>Annotationes in Locos communes</em> (1561) with rule-based entity annotations.</p>
  <p><a href="prototype/" style="display: inline-block; padding: 8px 20px; background: #3f51b5; color: white; border-radius: 4px; text-decoration: none; font-weight: 500;">Open Corpus Browser &rarr;</a></p>
</div>

## What This Prototype Demonstrates

This is a **Layer 1 prototype** — the first stage of the GNORM adaptation pipeline for Protestant theological texts:

| Feature | Description |
|---------|-------------|
| **Hierarchical navigation** | Browse by chapter (*locus*): PRAEFATIO, DE DEO, DE TRINITATE, etc. |
| **Rule-based entity detection** | Biblical, patristic, reformation, classical, and confessional references |
| **Epistemic indicators** | FACTUAL / INTERPRETIVE confidence levels on each detected reference |
| **Full-text search** | Search across the entire corpus with result highlighting |
| **Entity type filtering** | Toggle visibility of different reference types |

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

- **Pure HTML/CSS/JS** — no build step, no framework dependencies
- **Client-side rendering** — all data loaded from a single `corpus.json` file
- **Data generation** — `build_corpus_json.py` parses normalized text files with enhanced regex patterns
- **Hosted on GitHub Pages** — alongside the MkDocs documentation

## Next Steps

1. **Manual annotation in INCEpTION** — create training data for the CRF model
2. **CRF training** — adapt the GNORM CRF pipeline for Protestant theological texts
3. **Enhanced detection** — integrate CRF predictions into the corpus browser
4. **Citation network visualization** — D3.js graphs showing citation relationships

*Last updated: 2026-02-13*

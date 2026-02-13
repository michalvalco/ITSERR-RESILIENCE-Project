# Deep Read & Value Extraction: GEM and CHAT Reports

**Date:** February 14, 2026  
**Author:** Claude (for Michal Valčo)  
**Sources analyzed:**
- `Report (GEM) GNORM Pipeline and Visualization Research.docx` — 782 lines, ~6.2k words
- `Report (CHAT) Annotation Scripts – Input Formats and Requirements.docx` — 893 lines, ~7.5k words

**Compared against:**
- `pipeline_technical_reference.md` (PKB) — definitive pipeline reference, last updated Feb 13
- `workflow_diagram.md` (PKB / filesystem) — 7-stage adaptation workflow, revised Feb 13
- `itserr_reference_mapping.md` (PKB) — prototype agent architecture (no overlap expected)
- `Ethically-Grounded_AI_Agents...md` (PKB) — 142-source literature synthesis

---

## 1. Executive Summary

The reports add **moderate new value** in two specific areas — the 3D visualization stack and Omeka S integration — while confirming (with significant redundancy) our existing understanding of the pipeline. Roughly 70% of both reports restates what `pipeline_technical_reference.md` already covers from our Feb 13 code inspection, often with less precision. The genuinely new material concerns: (a) the GEM report's identification of the **ATON Framework** as the probable 3D visualization technology (plausible inference, not yet confirmed by Palermo team), and (b) both reports' detailed coverage of **Omeka S / W3C Web Annotation / IIIF** integration pathways, which our existing documents treat as a downstream concern without technical detail. There is one notable reference in the CHAT report to a GNORM paper on **Babylonian Talmud visualization** (Pavone & Imperia, 2025) that strengthens our adaptation thesis.

No corrections to our existing understanding were found. Several small technical details are worth extracting as surgical additions.

---

## 2. New Findings for `pipeline_technical_reference.md`

### Finding 2.1: `all_possible_states` / `all_possible_transitions` CRF parameters

- **What:** sklearn-crfsuite supports `CRF(all_possible_states=True, all_possible_transitions=True)` to consider label states or transition pairs not seen in training data. Potentially relevant when training multi-type models on small datasets where some B→I or type→type transitions might not appear in training examples.
- **Where in reference doc:** Section 3, after "Multi-Type Label Support" — or Section 8, under "Still TBD" (multi-entity CRF performance)
- **Source:** CHAT report, Section 4 (lines 248–251), referencing sklearn-crfsuite docs
- **Suggested text:**

> **Note on sparse training data:** When training multi-type models where some label transitions may not appear in training data (e.g., no example of `B-HYMN → I-HYMN`), consider setting `CRF(all_possible_states=True, all_possible_transitions=True)` in `train_crfsuite.py`. This allows the model to learn zero-initialized weights for unseen transitions rather than treating them as impossible. Relevant for our 7-type schema with inevitably small per-type training sets.

### Finding 2.2: Tokenization alignment requirement (explicit)

- **What:** Both reports emphasize that the tokenizer used for inference input *must match* the tokenization produced by `cas_to_bioes.py` during training data generation. If training data treats punctuation as separate tokens (which UIMA CAS tokenization typically does), inference input must replicate this exactly. Mismatch degrades model performance. The GEM report specifically recommends NLTK `WordPunctTokenizer` or a regex-based splitter aligned with `cas_to_bioes.py` behavior.
- **Where in reference doc:** Section 2, "Zero-Shot Test Strategy" — Path B currently describes creating a "minimal CAS XMI ZIP" but doesn't explicitly warn about tokenization alignment.
- **Source:** GEM report, Section 1.2.1 (lines 150–159); CHAT report, Section 1 (lines 18–24)
- **Suggested text (add to Path B description):**

> ⚠️ **Tokenization alignment critical:** Whatever tokenization method the bridge script uses *must replicate* the tokenization behavior of `cas_to_bioes.py` / UIMA CAS XMI. If training data splits punctuation as separate tokens (standard CAS behavior), inference input must match. Use NLTK `WordPunctTokenizer` or inspect `cas_to_bioes.py`'s tokenization logic directly. Mismatch between training and inference tokenization will degrade CRF accuracy even on in-domain text.

### Finding 2.3: Network scale of the GNORM output

- **What:** The GNORM annotation of the complete *Liber Extra* produced a network of approximately **1,795 unique legal source nodes** connected by **41,784 reference edges**. This gives concrete scale for the visualization challenge and helps calibrate expectations for Stöckel corpus output.
- **Where in reference doc:** Section 1, near the existing "41,784 legal references" mention — or as a new note
- **Source:** CHAT report, Section 7 (lines 635–636)
- **Suggested text (add after existing "41,784 legal references" mention):**

> The resulting citation network contains ~1,795 unique legal source nodes and ~41,784 reference edges — a scale that requires filtering/clustering for interactive visualization.

### Finding 2.4: 3D Visualization — probable ATON Framework identification

- **What:** The GEM report identifies the **ATON Framework** (CNR ISPC, developed by Bruno Fanini) as the likely 3D visualization technology for GNORM, based on institutional alignment (E-RIHS.it/H2IOSC), service listings, and technical profile. Tech stack: **Three.js** (frontend rendering), **Node.js** (backend), **REST API + WebSocket** (collaboration). Input formats: **glTF/glb** (single objects), **3D Tiles** (massive datasets), **NXS/NXZ** (multi-resolution via Nexus). Configuration via **JSON files** with SPARQL queries for dynamic metadata retrieval. GitHub: `phoenixbf/aton`.
- **Where in reference doc:** Section 7, "Adaptation Gaps" — under "3D visualization" row (currently says "Mentioned in ITSERR docs; absent from CIC_annotation code. Separate GNORM component?")
- **Source:** GEM report, Section 3 (lines 348–477)
- **Important caveat:** This is *inference from triangulation*, not confirmed by the Palermo team. The CHAT report is more cautious, noting that "publications do not explicitly name the software stack" and that CNR's Visual Computing Lab also has frameworks like 3DHOP and Nexus. **Must verify with Arianna.**
- **Suggested text (replace existing "3D visualization" row in Adaptation Gaps table):**

> | 3D visualization | Probable: ATON Framework (CNR ISPC, Bruno Fanini). Three.js frontend, Node.js backend, glTF/3D Tiles input, JSON config with SPARQL queries. GitHub: `phoenixbf/aton`. Also possible: 3DHOP/Nexus from CNR Visual Computing Lab. | ❓ | **Unconfirmed** — inferred from E-RIHS service listings and institutional alignment (GEM report triangulation). Needs verification with Arianna. CHAT report suggests custom Three.js/WebGL more likely than a specific framework. |

**Also add to Section 8 "Still TBD":**

> - 3D visualization component — GEM report identifies ATON Framework (CNR ISPC) as probable technology; CHAT report suggests custom Three.js/WebGL. **Ask Arianna:** Is the GNORM visualization built on ATON, 3DHOP, or a custom Three.js application? What input format (JSON config, SPARQL, static data)?

### Finding 2.5: GNORM applied to Babylonian Talmud (cross-domain precedent)

- **What:** Pavone and Imperia have published on extending GNORM conceptually to the Babylonian Talmud: "GNORM: Challenges and Potential of a 3D Visualisation of the Babylonian Talmud" (2025, in *The Digital Turn in Religious Studies*). This is significant: it demonstrates the GNORM team has already considered applying their approach to non-canon-law religious corpora. This directly strengthens our adaptation thesis.
- **Where in reference doc:** Section 1 (Pipeline Architecture Overview), as a context note — or new Section 8 entry
- **Source:** CHAT report, Section 3 (lines 188–192), referencing ResearchGate: `10.xxxx/398385581`
- **Suggested text (add to Section 1 or as new subsection):**

> ✅ **Cross-domain precedent:** Pavone & Imperia (2025), "GNORM: Challenges and Potential of a 3D Visualisation of the Babylonian Talmud" (in *The Digital Turn in Religious Studies*), demonstrates the GNORM team has already conceptualized extending the framework to non-canon-law religious corpora. This directly supports our adaptation to Protestant theological texts.

---

## 3. New Findings for `workflow_diagram.md`

### Finding 3.1: Omeka S integration architecture — W3C Web Annotation import

- **What:** Both reports provide detailed technical coverage of the Omeka S integration pathway that our workflow diagram treats as a future concern ("Stage 7 — mostly WP4 of the APVV grant"). Key details:
  - **Annotate module** (by Daniel Berthereau) implements W3C Web Annotation Data Model
  - Import via **CSV Import module** — columns map to RDF properties (`oa:hasTarget`, `oa:hasBody`, `oa:motivatedBy`)
  - Each pipeline reference becomes one `oa:Annotation` resource with Target (page/canvas), Body (citation text/URI), and optional Motivation
  - Selector (coordinate) data via `#xywh=x,y,w,h` fragment in target URI
  - Alternative: generate **IIIF Annotation Lists** as JSON-LD (IIIF Presentation API 3.0) directly, bypassing CSV
  - Current Annotate module limitation: "only one motivation, one body and one target are generally managed"
  - Omeka S 3.1+ required for compatibility
- **Where in workflow:** Stage 7 (Interact) — currently a high-level sketch
- **Source:** GEM report, Section 4 (lines 479–602); CHAT report, Section 5 (lines 272–520)
- **Suggested text (add to Stage 7):**

> **Technical integration path (from GEM/CHAT reports, to be validated):**
>
> Pipeline output → conversion script (`inference_to_csv.py` or `inference_to_iiif.py`) → two pathways:
>
> **Path 1: CSV Import (simpler).** Create CSV with columns mapped to W3C Web Annotation properties: `oa:hasTarget` (Omeka item ID or IIIF Canvas URI with `#xywh=` fragment for spatial selector), `oa:hasBody` (citation text or authority URI), `oa:motivatedBy` (e.g., `oa:identifying`). Import using Omeka S CSV Import module with the "Annotation" resource template. Requires Annotate module (Daniel Berthereau). Limitation: one body, one target per annotation.
>
> **Path 2: IIIF Annotation Lists (richer).** Generate JSON-LD files following IIIF Presentation API 3.0 — each page gets an AnnotationPage with Annotation items containing TextualBody and Canvas target with xywh selector. Requires IIIF Server module. More elegant for visual annotation overlay.
>
> **Decision needed:** Path 1 is simpler for bulk import; Path 2 is better for visual rendering. Can combine both (CSV for metadata, IIIF for visual layer).
>
> **Modules required:** Annotate, CSV Import, IIIF Server, IIIF Presentation. Omeka S v3.1+.

### Finding 3.2: digitaldecretals.com

- **What:** The CHAT report mentions `digitaldecretals.com` as an associated GNORM website, possibly hosting the corpus or an interface prototype. Not present in any of our current documents.
- **Where in workflow:** Stage 5 (Represent), near "Arianna demonstrated the GNORM prototype web interface at ariannapavone.com/gnorm/"
- **Source:** CHAT report, Section 3 (lines 181–184)
- **Suggested text (add after existing ariannapavone.com/gnorm reference):**

> Additionally, `digitaldecretals.com` appears associated with the GNORM project (possibly the text corpus or prototype; not yet verified).

---

## 4. New Findings for Other Documents

### Finding 4.1: For `Ethically-Grounded_AI_Agents...md` (literature synthesis)

The Pavone & Imperia (2025) paper on GNORM and the Babylonian Talmud should be added to the literature synthesis. Currently the synthesis references Waxman's Talmud graph database (2021) and Sefaria but does not mention GNORM's own cross-domain extension to Talmudic texts.

**Suggested addition to Section 4 (GNORM/ITSERR context):**

> Pavone, A. & Imperia, V. (2025). "GNORM: Challenges and Potential of a 3D Visualisation of the Babylonian Talmud." In *The Digital Turn in Religious Studies*. — Demonstrates cross-domain applicability of the GNORM framework beyond canon law. The team's exploration of Talmudic text visualization confirms that the methodology was designed with extensibility in mind. ResearchGate: [publication/398385581](https://www.researchgate.net/publication/398385581).

### Finding 4.2: Publication reference — Pavone "Challenges and Potential" chapter

Full citation for the GNORM visualization chapter (useful for bibliography):

> Pavone, A. & Imperia, V. (2025). "Challenges and Potential of a 3D Visualisation of the Corpus Iuris Canonici." In *The Digital Turn in Religious Studies*. OA Link: `http://hdl.handle.net/10447/695218`. — Details GNORM's theoretical and technological foundations, confirms prototype exists internally, describes "thematic filtering based on typological" categories.

---

## 5. Corrections

**No corrections found.** Our existing reference documents are more precise than the reports on every point where they overlap. Specifically:

- The reports describe the `cas_to_bioes.py` hardcoded `AN` issue and the `bioes_to_cas.py` hardcoded TypeSystem — both already captured in our Feb 13 code inspection findings.
- The reports describe the INCEpTION ZIP entry point requirement — already captured as a confirmed finding.
- The reports describe CRF label-agnosticism — already captured with `train_crfsuite.py` code-level detail.
- Both reports propose `text_to_inference_format.py` as a bridge script — already captured as "Path B (quick hack)" in our Zero-Shot Test Strategy.

**One mild framing discrepancy worth noting:** The GEM report states `text_to_inference_format.py` is "strictly required" (line 208). Our reference is more accurate: it's required *only for zero-shot testing or bypass scenarios*. The designed workflow is INCEpTION → `cas_to_bioes.py` → pipeline, which doesn't need a bridge script. The bridge is a convenience for testing, not a permanent architectural component.

---

## 6. Discarded Overlap (confirmed coverage)

The following topics are covered extensively in both reports but add nothing beyond what `pipeline_technical_reference.md` and `workflow_diagram.md` already contain:

- **BIOES/BILOU tagging scheme** — both reports explain at length. Already in Section 2.
- **6-layer pipeline architecture** — GEM Section 1.1 and CHAT Section 1 both describe. Already in Section 1.
- **INCEpTION roundtrip** (CAS XMI → BIOES → pipeline → CAS XMI) — extensively covered in both. Already in Section 2.
- **CRF label-agnosticism** — both reports confirm. Already in Section 3 with code-level detail.
- **`cas_to_bioes.py` hardcodes `AN`** — both mention. Already confirmed Feb 13 with line numbers.
- **`bioes_to_cas.py` hardcoded TypeSystem** — GEM Section 2.2 focuses on this. Already in Section 3.
- **Feature window ±6 tokens** — GEM Section 2.3 confirms. Already in Section 4 (via reference to full doc).
- **Character-level features missing** — GEM Section 2.3 recommends adding character n-grams. Already identified as adaptation gap.
- **`predict_marginals()` for epistemic classification** — GEM Section 2.4. Already in Section 5 with proposed dual-path design.
- **No raw `.txt` entry point** — both reports state emphatically. Already confirmed Feb 13.
- **CRF performance: 97.8% accuracy** — mentioned in passing by CHAT. Already documented.
- **Per-file modification requirements for multi-type support** — GEM Section 2.2 discusses `bioes_to_cas.py`. Already detailed in Section 3 table.

**On GNORM visualization screenshots:** The prompt specifically asked about screenshots. The GEM report contains `media/image1.png` through `media/image5.png` references, but these are mathematical formula images (LaTeX-rendered equations for CRF feature functions), **not** screenshots of the GNORM 3D visualization. The CHAT report contains no images. So: **no visualization screenshots found in either report.**

---

## Summary Action Items

| Priority | Action | Target Document |
|----------|--------|-----------------|
| **HIGH** | Add ATON Framework identification (with caveat) + update open questions | `pipeline_technical_reference.md` §7, §8 |
| **HIGH** | Add Omeka S / W3C Web Annotation integration details | `workflow_diagram.md` Stage 7 |
| MEDIUM | Add tokenization alignment warning to Path B | `pipeline_technical_reference.md` §2 |
| MEDIUM | Add `all_possible_states`/`transitions` note | `pipeline_technical_reference.md` §3 or §8 |
| MEDIUM | Add Pavone & Imperia Talmud paper as cross-domain precedent | `pipeline_technical_reference.md` §1; `Ethically-Grounded...md` §4 |
| LOW | Add network scale note (1,795 nodes / 41,784 edges) | `pipeline_technical_reference.md` §1 |
| LOW | Add `digitaldecretals.com` reference | `workflow_diagram.md` Stage 5 |
| LOW | Add full Pavone visualization chapter citation | bibliography / reference list |

---

*Analysis prepared for the ITSERR TNA Fellowship project. For current project status see `TNA_FELLOWSHIP_HUB.md`.*

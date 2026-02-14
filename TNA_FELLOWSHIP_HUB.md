# TNA Fellowship Hub

**Fellowship:** ITSERR TNA, University of Palermo, Feb 10–27, 2026
**Fellow:** Prof. Michal Valčo (ELTF, Comenius University Bratislava)
**Last updated:** February 14, 2026

---

## Current Status (overwrite after each session)

**Date:** Feb 14, 2026 (Day 5 of 14)
**Active work:** Corpus Browser enhanced (dashboard, three-column layout, 31 references across 5 entity types). Abbreviation provenance architecture implemented (expansion_log bridges Stage 2→Stage 4 Layer 2). XML tag pollution fixed in zero-shot CRF experiment. Comprehensive documentation audit completed across all repo docs. 413 tests passing (incl. 21 for build_corpus_json.py consensus/epistemic logic).
**Next:** (1) Revision pass on working paper — citation verification, redundancy removal. (2) Prepare consortium presentation materials (Feb 25). (3) Zero-shot test on Stöckel sample. (4) Next in-person meeting with Arianna/Marcello.
**Blockers:** None currently.

---

## The Pivot (Feb 12 — Foundational Context)

The TNA application promised an **AI agent prototype with personalist ethics framework**. After the first meeting with Arianna and Marcello (Feb 12), the focus shifted to **GNORM pipeline adaptation for the Stöckel corpus**, with the personalist philosophical framework as the bridging contribution.

These are not contradictory — the epistemological classification (FACTUAL/INTERPRETIVE/DEFERRED) bridges them — but the emphasis has shifted substantially toward hands-on digital humanities methodology.

**For hosts:** Frame as: "The ethical framework I proposed requires concrete technical grounding. Rather than building abstract principles, I'm testing them against a real adaptation challenge — applying your GNORM pipeline to a new domain. The epistemic modesty indicators I proposed map directly onto the `mark_source` mechanism in your pipeline."

**For ITSERR reporting:** The blog post and final report should show both dimensions — the philosophical framing AND the technical adaptation work.

---

## Active Workstreams

| # | Workstream | Tracked In | Status |
|---|-----------|-----------|--------|
| 1 | **Integrated Research Synthesis** | `docs/resources/integrated_report_strategy.md` | ✅ INTEGRATION PASS COMPLETE. Draft (~15.5K words, 9 sections + 80 bibliography entries) integrity-checked. Next: revision pass. |
| 2 | **GNORM/Stöckel Workflow** | `01_research/workflow_diagram.md` | Workflow diagram complete (7 stages) with abbreviation provenance architecture (Stage 2 → Stage 4 Layer 2 data flow). Next: zero-shot test, entity schema validation |
| 3 | **Writing & Deliverables** | `02_writing/` | Full synthesis draft complete (`tna_working_paper_draft.md`). Blog post skeleton exists. Consortium presentation TBD (Feb 25/27) |
| 4 | **Prototype** | `03_prototype/` + `stockel_annotation/PROGRESS.md` | OCR pipeline scripts (`ocr_processor`, `extract_alto`, `normalize_text`), corpus data generator (`build_corpus_json`), ML pipeline (`cas_to_bioes`, `zero_shot_crf`), Corpus Browser with dashboard and 31 detected references. Abbreviation expansion provenance logging for Stage 4 Layer 2. 393 tests passing across 10 suites. See `PROGRESS.md` for detailed tracker |

---

## Where Things Live

### Repositories

| Repo | Path | Role |
|------|------|------|
| **ITSERR-RESILIENCE-Project** | `GitHub\ITSERR-RESILIENCE-Project\` | Primary fellowship workspace: research, writing, prototype, presentations |
| **APVV-2026-Religiozne-Dedicstvo** | `GitHub\APVV-2026-Religiozne-Dedicstvo\` | Grant-specific: CIC Deep Dive, SNK correspondence, team CVs, GNORM audit |
| **CIC_annotation** | `GitHub\CIC_annotation\` | Source pipeline code (Esuli et al.). Do not modify; fork if needed |
| **Claude_Protocols** | `GitHub\Claude_Protocols\` | General collaboration infrastructure: research paper protocol, quality standards, decision framework |

### Working Directory (local, not in any repo)

`C:\Users\valco\OneDrive\Documents\04 Projekty\2025 ITSERR - Resilience Project\`

| Content | Subfolder |
|---------|-----------|
| Source reports for synthesis (.docx) | `Resources\` |
| Synthesis outline & strategy (also synced to ITSERR repo) | `Resources\` |
| Source PDFs (academic papers) | `Resources\` |
| Meeting transcripts | Root |
| TNA application materials | `TNA Application\` |
| Collaborator profiles | `TNA Collaborators Profiles\` |
| Travel logistics | `TNA Logistics\` |
| Marcello's Miro workflow screenshot | Root |

### Key Documents by Purpose

#### Technical Documentation (GNORM / Pipeline)

| Document | Location | Notes |
|----------|----------|-------|
| CIC_annotation Deep Dive (line-by-line code analysis) | `APVV repo: 06_technologie/CIC_annotation_Deep_Dive_Report.md` | 567 lines. Authoritative reference for pipeline architecture |
| GNORM Technical Audit for SNK | `APVV repo: 06_technologie/GNORM_Technical_Audit_for_SNK.md` | Written for SNK audience |
| SNK Response (Glončák) | `APVV repo: 06_technologie/Odpoved_Gloncak_SNK.md` | Infrastructure constraints |
| Beginner's Guide for team | `APVV repo: 08_zdroje/Beginners_Guide_GNORM_Adaptation.md` | For Hanus, Kowalská, Kollárová |
| Epistemic Modesty Framework | `ITSERR repo: 01_research/epistemic_modesty_framework.md` | FACTUAL/INTERPRETIVE/DEFERRED classification |
| Workflow Diagram (7 stages) | `ITSERR repo: 01_research/workflow_diagram.md` | Based on Marcello's Fry 2007 framework |
| CIC_annotation source code | `CIC_annotation repo` (all .py files) | The actual pipeline |
| Stöckel pilot workspace | `ITSERR repo: 03_prototype/stockel_annotation/` | Where zero-shot test and adaptations will live |
| **Progress Tracker** | `ITSERR repo: 03_prototype/stockel_annotation/PROGRESS.md` | **Definitive reference for what's built and tested.** All scripts, test results (393 tests across 10 suites), OCR quality assessment, data flow, dependencies. Consult when asking "what do we have?" or "does X work?" |

#### Research Synthesis

| Document | Location | Notes |
|----------|----------|-------|
| Source A: Claude Report (~142 sources) | PKB + `Resources\Ethically-Grounded AI Agents...` | Comprehensive literature landscape |
| Source B: GEM Report (~33 sources) | `Resources\AI Agents for Religious Studies (GEM) Report.docx` | V4 infrastructure, theological metaphors |
| Source C: Chat Report | `Resources\Report (CHAT) - Towards an Ethically-Grounded AI Research Assistant.docx` | Third source, ✅ integrated Feb 14 |
| Integration strategy & session log | `ITSERR repo: docs/resources/integrated_report_strategy.md` | Also synced to `Resources\` |
| Detailed outline (~680 lines) | `ITSERR repo: docs/resources/integrated_report_detailed_outline.md` | Also synced to `Resources\` |
| Integration prompt for [C] | `Resources\PROMPT_integrate_chat_report.md` | Handoff prompt for fresh context window — ✅ executed Feb 14 |
| **Working paper draft** | `ITSERR repo: 02_writing/working_paper/tna_working_paper_draft.md` | ~16–17K words, 9 sections. All drafting complete; needs bibliography, integration pass, revision. |

#### Fellowship Planning & Meetings

| Document | Location | Notes |
|----------|----------|-------|
| TNA Working Agenda & Questions (32 questions) | `APVV repo: 06_technologie/TNA Fellowship Working Agenda and Questions.md` | ⚠️ Hold — send to Arianna after trust established, not before |
| Meeting transcript (Arianna + Marcello, 12 Feb) | `Local: Transcript - Arianna Pavone and Marcello Costa meeting Feb 12 - summarized.docx` | Key takeaways: workflow-first, Miro, format interoperability |
| Collaborator profiles | `Local: TNA Collaborators Profiles\` | Background on Arianna, Marcello, Andrea |
| TNA Application (original) | `Local: TNA Application\` | What hosts expect vs. what we're actually doing |
| Marcello's workflow template | `Local: Workflow Draft - on Miro - from Marcello.png` | Miro framework screenshot |

#### Stöckel Source Materials

| Resource | Location | Notes |
|----------|----------|-------|
| Stöckel digitised works | `06 Resources/Dejiny/Domace cirkevne dejiny/Leonard Stoeckel/Diela Stoeckela/` | Raw TIFFs and PDFs |
| KEGA Stöckel project materials | `04 Projekty/2021 KEGA Stockel/` | Earlier project; may contain transcriptions |
| Stöckel annotation pilot | `ITSERR repo: 03_prototype/stockel_annotation/` | Pipeline test workspace |

#### APVV Grant (Reference)

| Document | Location | Notes |
|----------|----------|-------|
| Submitted application | `APVV repo: 01_ziadost/komplet/application-APVV-25-0349.pdf` | 198,220 EUR, 48 months |
| English research plan | `APVV repo: 01_ziadost/komplet/vecny-zamer-en-1243-2026-2-06.pdf` | Use when explaining project to Palermo team |
| Project stages and milestones | `APVV repo: 01_ziadost/komplet/05_etapy_projektu.md` | 4-year plan with WP structure |

---

## Marcello's Key Requirements (from 12 Feb meeting)

1. **Workflow diagram** — using his Acquire → Parse → Filter → Mine → Represent → Refine → Interact framework. ✅ Done: `01_research/workflow_diagram.md`
2. **Data format commitment** — Markdown, CSV, JSON, XML only. No .docx for working documents.
3. **Target users defined** — who generates value, who consumes it, domain context. ✅ Done: in workflow diagram.
4. **Rough draft on Miro canvas** — populate his template. Basis for next in-person meeting.

---

## Claude Project PKB Contents (static reference files)

| File | Purpose | When to consult |
|------|---------|----------------|
| `Ethically-Grounded_AI_Agents...md` | Source A: 142-source literature landscape, five-gap analysis | Literature questions, citation lookups, gap framing |
| `itserr_reference_mapping.md` | Prototype architecture snapshot (Jan 25) | Agent code architecture, test coverage, technical debt |
| `pipeline_technical_reference.md` | CIC/GNORM pipeline essentials for adaptation | Any technical pipeline work, entity schemas, BIOES format |

These are static snapshots. For current status, always read this HUB file and `integrated_report_strategy.md` from the filesystem.

---

## Interoperability Commitments

| Principle | Implementation |
|-----------|---------------|
| No proprietary formats for working documents | Markdown, CSV, JSON, XML only (per Marcello) |
| Version control | Git (ITSERR and APVV repos) |
| FAIR data principles | Metadata, persistent identifiers, open formats |
| Reproducibility | Pipeline scripts, configuration files, documented parameters |

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 12 Feb 2026 | Pivot TNA focus from AI agent prototype to GNORM pipeline adaptation | Aligns with APVV grant core methodology; more concrete deliverables; directly serves Stöckel corpus work |
| 12 Feb 2026 | Designate ITSERR repo as primary TNA workspace | Prevents fragmentation across repos and local folders |
| 12 Feb 2026 | Hold Working Agenda document until after trust established | Marcello wants workflow-first approach; 32 questions would overwhelm before relationship built |
| 12 Feb 2026 | Adopt interoperable formats (Markdown, CSV, JSON) for all new work | Per Marcello's explicit guidance; FAIR principles |
| 13 Feb 2026 | Reorganize Claude Project: PKB for static references only, Instructions point to filesystem for current state | Prevents stale status info; HUB and strategy doc always read fresh from disk |
| 13 Feb 2026 | Replace daily_log.md with lean status section in HUB | Empty 613-line template wasn't being used; session log in strategy doc serves as detailed record |
| 13 Feb 2026 | Plan pipeline_technical_reference.md for PKB | Condensed CIC/GNORM essentials (~200 lines) for quick context in every technical conversation |
| 13 Feb 2026 | Use `stockel_annotation/PROGRESS.md` as detailed prototype reference | Too granular for HUB (per-script docs, test results, OCR quality specifics). Lives alongside the code it documents; HUB points to it in Key Documents and Workstream 4 |
| 14 Feb 2026 | Deep read analysis of GEM + CHAT reports | ~70% overlap with existing knowledge confirmed. New findings: ATON Framework identification (unconfirmed), Omeka S/IIIF integration details, Pavone & Imperia Talmud paper as cross-domain precedent. No corrections needed. 8 surgical additions queued for live docs. |
| 14 Feb 2026 | Upload `deep_read_GEM_CHAT_analysis.md` to PKB | Provides cross-report analysis as persistent context for all sessions |
| 14 Feb 2026 | Apply all 8 deep read additions to live docs | `pipeline_technical_reference.md` (6 edits) and `workflow_diagram.md` (2 edits). PKB copies remain as static snapshots — live docs on filesystem are now ahead of PKB. |
| 14 Feb 2026 | Source [C] integration complete | ChatGPT report assessed (~70% redundant, ~15–18 genuinely new sources) and integrated into detailed outline. Key additions: Caffagni et al. (BERT for biblical refs), Detweiler (Protestant computational hermeneutics), Adeboye et al. (cross-religious reductionism), Zimmermann (personalist tech ethics), Tripitaka Koreana 3D viz. Assessment saved as `chat_report_assessment.md`. Phase 1 of synthesis now complete. |
| 14 Feb 2026 | Synthesis drafting complete (§1–§9) | All 9 sections drafted (~16–17K words) in `tna_working_paper_draft.md`. Renamed from `integrated_research_synthesis.md` to avoid confusion with Source [A] PKB file. Next: bibliography assembly, integration pass, revision pass. |
| 14 Feb 2026 | Integration pass complete | Full integrity check performed: (1) source count corrected (142→"over 80" — actual bibliography entries); (2) orphan citation resolved (Wang et al. 2024 added to §2.2; Puccetti 2024 ERCIM removed as redundant); (3) all cross-references verified consistent; (4) five-gap threading confirmed across §1→§2→§4→§5→§6→§9; (5) voice consistency confirmed throughout. Draft status updated to "integration pass complete." |
| 14 Feb 2026 | Abbreviation provenance: `expansion_log` on NormalizationStats | Resolves the "Abbreviation Logic Conflict" between Stage 2 (PARSE) and Stage 4 (MINE). `normalize_text.py` expands abbreviations (dñs→dominus etc.) for clean text, but now logs each expansion with original form, expanded form, character offset, and regex pattern. Stage 4 Layer 2 can consume this log directly as "detected via abbreviation dictionary" evidence without re-scanning expanded text. Documented in `workflow_diagram.md` Stage 2 and Stage 4 sections. |
| 14 Feb 2026 | XML tag stripping in zero-shot CRF experiment | `normalize_text.py` injects `<ref type="...">` tags into output; `zero_shot_crf_experiment.py` was tokenising these as garbage tokens polluting the CRF context window. Added `strip_ref_tags()` before tokenisation (same pattern as `build_corpus_json.py`). |
| 14 Feb 2026 | Comprehensive documentation audit | Cross-referenced all 8+ documentation files against actual repo state. Fixed outdated test counts (163/296→389), missing scripts, incorrect statuses, phantom TECHNOLOGY_INVENTORY.md reference, and missing Corpus Browser features across README, HUB, PROGRESS.md, pipeline/overview.md, corpus-browser.md, and index.md. |

---

## Session End Protocol

1. **If synthesis work done:** Append session entry to `integrated_report_strategy.md` Section 8
2. **Always:** Overwrite the "Current Status" section at top of this file
3. **If strategic decisions made:** Append to Decision Log above
4. **New files:** Place in correct repo/directory per topology above

---

*This document is the single source of navigation for the TNA Fellowship. Keep it current.*

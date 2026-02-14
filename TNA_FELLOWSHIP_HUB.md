# TNA Fellowship Hub

**Fellowship:** ITSERR TNA, University of Palermo, Feb 10–27, 2026
**Fellow:** Prof. Michal Valčo (ELTF, Comenius University Bratislava)
**Last updated:** February 14, 2026

---

## Current Status (overwrite after each session)

**Date:** Feb 14, 2026 (Day 5 of 14)
**Active work:** Source [C] (ChatGPT report) fully integrated into detailed outline. All three source reports now merged into single 680+ line outline with [A]/[B]/[C] attribution tags throughout. Assessment document created (`chat_report_assessment.md`). ~9 new sources added to bibliography assembly notes. Both working directory and GitHub copies synced.
**Next:** Phase 2 drafting of synthesis sections (begin with §2, §3, §6 as highest priority). Prepare for next in-person meeting with Arianna/Marcello. Two PKB-only items remain as TODOs for synthesis drafting: (1) Pavone & Imperia Talmud paper addition to literature synthesis, (2) full Pavone visualization chapter citation.
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
| 1 | **Integrated Research Synthesis** | `docs/resources/integrated_report_strategy.md` | ✅ Phase 1 complete (all three sources integrated). Outline at ~680 lines with [A]/[B]/[C] tags. ~160–170 sources catalogued. Ready for Phase 2 section drafting. |
| 2 | **GNORM/Stöckel Workflow** | `01_research/workflow_diagram.md` | Workflow diagram complete (7 stages). Next: zero-shot test, entity schema validation |
| 3 | **Writing & Deliverables** | `02_writing/` | Working paper sections drafted (pre-pivot). Blog post skeleton exists. Consortium presentation TBD (Feb 25/27) |
| 4 | **Prototype** | `03_prototype/` + `TECHNOLOGY_INVENTORY.md` | Functional but secondary to pipeline work. Full inventory of scripts, tests (163 passing), OCR results, and quality assessment in `TECHNOLOGY_INVENTORY.md` |

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
| **Technology Inventory** | `ITSERR repo: 03_prototype/TECHNOLOGY_INVENTORY.md` | **Definitive reference for what's built and tested in 03_prototype/.** All scripts, test results (163 tests), OCR quality assessment, data flow, dependencies. Consult when asking "what do we have?" or "does X work?" |

#### Research Synthesis

| Document | Location | Notes |
|----------|----------|-------|
| Source A: Claude Report (~142 sources) | PKB + `Resources\Ethically-Grounded AI Agents...` | Comprehensive literature landscape |
| Source B: GEM Report (~33 sources) | `Resources\AI Agents for Religious Studies (GEM) Report.docx` | V4 infrastructure, theological metaphors |
| Source C: Chat Report | `Resources\Report (CHAT) - Towards an Ethically-Grounded AI Research Assistant.docx` | Third source, ✅ integrated Feb 14 |
| Integration strategy & session log | `ITSERR repo: docs/resources/integrated_report_strategy.md` | Also synced to `Resources\` |
| Detailed outline (~680 lines) | `ITSERR repo: docs/resources/integrated_report_detailed_outline.md` | Also synced to `Resources\` |
| Integration prompt for [C] | `Resources\PROMPT_integrate_chat_report.md` | Handoff prompt for fresh context window — ✅ executed Feb 14 |

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
| 13 Feb 2026 | Create `03_prototype/TECHNOLOGY_INVENTORY.md` as detailed reference | Too granular for HUB (per-script docs, 163 test results, OCR quality specifics). Lives alongside the code it documents; HUB points to it in Key Documents and Workstream 4 |
| 14 Feb 2026 | Deep read analysis of GEM + CHAT reports | ~70% overlap with existing knowledge confirmed. New findings: ATON Framework identification (unconfirmed), Omeka S/IIIF integration details, Pavone & Imperia Talmud paper as cross-domain precedent. No corrections needed. 8 surgical additions queued for live docs. |
| 14 Feb 2026 | Upload `deep_read_GEM_CHAT_analysis.md` to PKB | Provides cross-report analysis as persistent context for all sessions |
| 14 Feb 2026 | Apply all 8 deep read additions to live docs | `pipeline_technical_reference.md` (6 edits) and `workflow_diagram.md` (2 edits). PKB copies remain as static snapshots — live docs on filesystem are now ahead of PKB. |
| 14 Feb 2026 | Source [C] integration complete | ChatGPT report assessed (~70% redundant, ~15–18 genuinely new sources) and integrated into detailed outline. Key additions: Caffagni et al. (BERT for biblical refs), Detweiler (Protestant computational hermeneutics), Adeboye et al. (cross-religious reductionism), Zimmermann (personalist tech ethics), Tripitaka Koreana 3D viz. Assessment saved as `chat_report_assessment.md`. Phase 1 of synthesis now complete. |

---

## Session End Protocol

1. **If synthesis work done:** Append session entry to `integrated_report_strategy.md` Section 8
2. **Always:** Overwrite the "Current Status" section at top of this file
3. **If strategic decisions made:** Append to Decision Log above
4. **New files:** Place in correct repo/directory per topology above

---

*This document is the single source of navigation for the TNA Fellowship. Keep it current.*


### Where Things Actually Live

#### Technical Documentation (GNORM / Pipeline)

| Document | Location | Notes |
|----------|----------|-------|
| CIC_annotation Deep Dive (line-by-line code analysis) | `APVV repo: 06_technologie/CIC_annotation_Deep_Dive_Report.md` | Comprehensive. Authoritative reference for pipeline architecture. |
| GNORM Technical Audit for SNK | `APVV repo: 06_technologie/GNORM_Technical_Audit_for_SNK.md` | Written for SNK audience; useful for interoperability questions |
| SNK Response (Glončák) | `APVV repo: 06_technologie/Odpoved_Gloncak_SNK.md` | Infrastructure constraints and integration requirements |
| Beginner's Guide for team | `APVV repo: 08_zdroje/Beginners_Guide_GNORM_Adaptation.md` | For Hanus, Kowalská, Kollárová — non-technical overview |
| Epistemic Modesty Framework | `This repo: 01_research/epistemic_modesty_framework.md` | FACTUAL/INTERPRETIVE/DEFERRED classification |
| CIC_annotation source code | `CIC_annotation repo` (all .py files) | The actual pipeline. Do not modify; fork if needed. |
| Stöckel pilot workspace | `This repo: 03_prototype/stockel_annotation/` | Where zero-shot test and adaptations will live |

#### Fellowship Planning

| Document | Location | Notes |
|----------|----------|-------|
| **TNA Working Agenda & Questions** (32 questions, 6 work items) | `APVV repo: 06_technologie/TNA Fellowship Working Agenda and Questions.md` AND `Local: 04 Projekty/ITSERR/TNA Fellowship Working Agenda and Questions.md` | ⚠️ DUPLICATE. APVV repo version is canonical. Hold this document — send to Arianna *after* next week's meeting, not before. |
| Meeting transcript (Arianna + Marcello, 12 Feb) | `Local: 04 Projekty/ITSERR/Transcript - Arianna Pavone and Marcello Costa meeting Feb 12 - summarized.docx` | Key takeaways: workflow-first approach, Miro canvas, format interoperability |
| Collaborator profiles | `Local: 04 Projekty/ITSERR/TNA Collaborators Profiles/` | Background on Arianna, Marcello, Andrea |
| TNA Application (original) | `Local: 04 Projekty/ITSERR/TNA Application/` | The original proposal. Context for what hosts expect vs. what we're actually doing. |
| Marcello's workflow template | `Local: 04 Projekty/ITSERR/Workflow Draft - on Miro - from Marcello.png` | Screenshot of the Miro framework. Basis for our workflow diagram. |

#### APVV Grant (Reference)

| Document | Location | Notes |
|----------|----------|-------|
| Submitted application | `APVV repo: 01_ziadost/komplet/application-APVV-25-0349.pdf` | Final submitted version. 198,220 EUR, 48 months. |
| English research plan | `APVV repo: 01_ziadost/komplet/vecny-zamer-en-1243-2026-2-06.pdf` | Use this when explaining the project to Palermo team |
| Status file | `APVV repo: STATUS.md` | Post-submission state, team, budget, timeline |
| Project stages and milestones | `APVV repo: 01_ziadost/komplet/05_etapy_projektu.md` | 4-year plan with WP structure |

#### Stöckel Source Materials

| Resource | Location | Notes |
|----------|----------|-------|
| Stöckel digitised works | `Local: 06 Resources/Dejiny/Domace cirkevne dejiny/Leonard Stoeckel/Diela Stoeckela/` | Raw source materials — TIFFs and PDFs |
| KEGA Stöckel project materials | `Local: 04 Projekty/2021 KEGA Stockel/` | Earlier project; may contain transcriptions |
| Stöckel annotation pilot | `This repo: 03_prototype/stockel_annotation/` | Pipeline test workspace |

---

## The Pivot: Bridging TNA Application and Actual Work

The TNA application promised an **AI agent prototype with personalist ethics framework**. The actual work focuses on **GNORM pipeline adaptation for Stöckel corpus**. These are not contradictory — the epistemological classification (FACTUAL/INTERPRETIVE/DEFERRED) bridges them — but the emphasis has shifted substantially toward hands-on digital humanities methodology.

**For hosts:** Frame this as: "The ethical framework I proposed requires concrete technical grounding. Rather than building abstract principles, I'm testing them against a real adaptation challenge — applying your GNORM pipeline to a new domain. The epistemic modesty indicators I proposed map directly onto the `mark_source` mechanism in your pipeline."

**For ITSERR reporting:** The blog post and final report should show both dimensions — the philosophical framing AND the technical adaptation work. The prototype in `03_prototype/` can evolve to demonstrate both.

---

## Marcello's Key Requirements (from 12 Feb meeting)

Marcello was clear about what he needs from you before productive collaboration can happen:

1. **Workflow diagram** — using his Acquire → Parse → Filter → Mine → Represent → Refine → Interact framework. Not a technology list; a process map. → See `01_research/workflow_diagram.md`

2. **Data format commitment** — stop using .docx for working documents. Use Markdown, CSV, JSON, XML. Marcello was explicit: Word and PDF are interoperability dead ends.

3. **Target users defined** — who generates value, who consumes it, what is the domain context?

4. **Rough draft on Miro canvas** — populate his template with your ideas, even if rough. This becomes the basis for next week's in-person meeting.

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 12 Feb 2026 | Pivot TNA focus from AI agent prototype to GNORM adaptation | Aligns with APVV grant core methodology; more concrete deliverables; directly serves Stöckel corpus work |
| 12 Feb 2026 | Designate ITSERR repo as primary TNA workspace | Prevents further fragmentation across APVV repo and local folders |
| 12 Feb 2026 | Hold Working Agenda document until after first in-person meeting | Marcello wants workflow-first approach; 32 questions would overwhelm before trust is established |
| 12 Feb 2026 | Adopt interoperable formats (Markdown, CSV, JSON) for all new work | Per Marcello's explicit guidance; aligns with FAIR principles |

---

## How to Use This Document

**Starting a work session:** Open this file. Check Timeline and Deliverables. Identify what's next. Navigate to the linked document/folder.

**After a significant meeting or work session:** Update the Decision Log and deliverable status. Note anything that changes the resource map.

**When confused about where something is:** Check the Resource Map. If it's not listed, it either doesn't exist yet or it's been missed — add it.

**When creating new files:** Put them in this repo unless they're pure logistics (travel, correspondence → local folder) or protocol-level (→ Claude_Protocols).

---

*This document is the single source of navigation for the TNA Fellowship. Keep it current.*

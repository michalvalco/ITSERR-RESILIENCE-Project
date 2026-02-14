# INTEGRATED RESEARCH SYNTHESIS: Development Strategy & Session Continuity

**Document purpose:** Cross-session reference for building the integrated report from three source documents. Add this file to the Claude Project Knowledge Base so it persists.

**Created:** February 10, 2026 (Day 1, Palermo)  
**Last updated:** February 13, 2026  
**Status:** Phase 1 complete; Phase 2 searches complete; integrating third source [C] before drafting

---

## 1. WHAT WE'RE BUILDING

**Output:** A single integrated research synthesis report that replaces all three source documents as the standard reference for the ITSERR TNA fellowship project.

**Working title:** *Designing Ethically-Grounded AI Agents for Religious Studies Research: A Comprehensive Research Synthesis*

**Target length:** ~15,000–20,000 words (the three sources combined are ~35,000+ words with significant overlap)

**Format:** Markdown (.md), suitable for later conversion to .docx for formal submission

**Audience (multiple):**
- Primary: Prof. Valčo himself — as working reference throughout and beyond fellowship
- Secondary: ITSERR Fellowship Board / consortium partners (formal deliverable context)
- Tertiary: Future publication drafts (the synthesis feeds into journal articles)

---

## 2. SOURCE DOCUMENTS

### Source A: "Claude Report" (the .md file in PKB)
- **Full title:** *Ethically-Grounded AI Agents for Religious Studies: A Research Synthesis on Agent Architectures, Computational Hermeneutics, and Personalist Design*
- **PKB filename:** `Ethically-Grounded_AI_Agents_for_Religious_Studies__A_Research_Synthesis_on_Agent_Architectures__Computational_Hermeneutics__and_Personalist_Design.md`
- **Sources cited:** ~142
- **Sections:** 5 major sections + conclusion with five-gap analysis
- **Strengths:** Rigorous full citations with DOIs; specific gap identification per section; named research groups with tables; priority reading lists per section; five-gap convergence analysis; graduated autonomy mapping (L1–L5); three-tier epistemic classification; specific prototype architecture recommendation; Prof. Valčo's own published work positioned
- **Weaknesses:** Dense academic prose; buries epistemic modesty inside Section 1; lacks V4/CEE infrastructure comparison; less accessible theological metaphors

### Source B: "GEM Report" (the .docx file)
- **Full title:** *Designing Ethically-Grounded AI Agents for Religious Studies Research: Architectures, Hermeneutics, and Infrastructure*
- **Filesystem path:** `C:\Users\valco\OneDrive\Documents\04 Projekty\2025 ITSERR - Resilience Project\Resources\AI Agents for Religious Studies (GEM) Report.docx`
- **Sources cited:** ~33
- **Sections:** 7 numbered sections + citation index
- **Strengths:** Vivid theological metaphors ("State as Locus," "Digital Dialectics," "Shadow of the Agent," "Pixelated Text"); clean comparative tables (Table 1: frameworks; Table 2: European infrastructure); V4 infrastructure comparison (Poland, Czechia, Slovakia, Hungary); Jungian framing for epistemic modesty; accessible introduction framing ("from search to synthesis," "third horizon")
- **Weaknesses:** Fewer and less precise citations (many are blog posts / web pages); some claims overstated (e.g., "CRFs outperformed Latin BERT by over 5%" without domain qualification); smaller scholarly footprint; no priority readings; no gap analysis

### Source C: "Chat Report" (the .docx file) — **NEW, pending integration**
- **Full title:** *Towards an Ethically-Grounded AI Research Assistant* (working title — to be confirmed after deep reading)
- **Filesystem path:** `C:\Users\valco\OneDrive\Documents\04 Projekty\2025 ITSERR - Resilience Project\Resources\Report (CHAT) - Towards an Ethically-Grounded AI Research Assistant.docx`
- **File size:** 436 KB
- **Sources cited:** TBD
- **Sections:** TBD
- **Strengths:** TBD — requires deep reading (see PROMPT_integrate_chat_report.md)
- **Weaknesses:** TBD
- **Integration status:** Not yet assessed. Prompt prepared for next session.

### Overlap Map (~40% redundant content between [A] and [B]; [C] overlap TBD)
These topics appear in both [A] and [B] and need merging (not duplication):
- Agent framework comparison (LangGraph, CrewAI, AutoGen)
- GNORM / CRF analysis and 3D visualization
- Gadamer / Ricoeur hermeneutics
- Techno-Gnosticism (Donati)
- Christian Personalism as design ethic
- MCP (Model Context Protocol)
- ITSERR work packages (WP3, WP4, WP6, WP8, WP9)
- Narrative memory / Zettelkasten concepts

### Tension Points Requiring Reconciliation
1. **Epistemic modesty framing:** GEM uses Jungian "Shadow" metaphor; Claude uses semantic entropy + calibrated confidence. → Layer both: Jungian as philosophical motivation, semantic entropy as technical implementation.
2. **CRF vs. Transformer claims:** GEM overstates CRF superiority; Claude is more precise about domain-specificity. → Use Claude's nuanced treatment; keep GEM's accessibility.
3. **Hermeneutics depth:** GEM gives accessible Gadamer/Ricoeur; Claude gives scholarly genealogy (Capurro → Romele → Hornby → Picca). → Merge: genealogy as backbone, GEM's faith/suspicion distinction as theological application.
4. **Source quality:** Several GEM citations are blog posts or Scribd links. → Flag these for replacement with scholarly sources where possible; retain only where content is unique and verifiable.
5. **[C] tensions:** TBD after deep reading of Chat report.

---

## 3. PROPOSED STRUCTURE (9 sections + bibliography)

### Section 1: Introduction — The Theological Turn in Artificial Intelligence
- **Source priority:** GEM framing ("from search to synthesis," "third horizon," "agentification") + Claude's scholarly precision + [C] TBD
- **Key moves:** Establish the five-domain structure; frame the contribution as bridging a genuine gap; introduce the fellowship context
- **Estimated length:** 800–1,000 words

### Section 2: AI Agent Architectures for Interpretive Humanities Work
- **Source priority:** Claude (computational hermeneutics opening: Kommers et al., Piotrowski, Mohr/Wagner-Pacifici) → framework comparison (Claude's detail + GEM's Table 1 + theological metaphors) → narrative memory (Claude's A-MEM/Zep/MemGPT + GEM's "Agentic Zettelkasten" label)
- **Unique GEM material to preserve:** "State as Locus" metaphor; "Digital Dialectics" / Scholastic Method for AutoGen; Table 1 (comparative framework analysis)
- **Unique Claude material to preserve:** Computational hermeneutics as paradigm; Elrod (2024) on LLM theological bias; CUNY agentic AI course; A-MEM Zettelkasten; Zep temporal knowledge graphs; "no published work applies multi-agent orchestration to theological/religious studies" gap statement
- **[C] material:** TBD
- **Estimated length:** 3,000–3,500 words

### Section 3: Epistemic Modesty and Calibrated Confidence
- **Rationale for standalone section:** Both reports treat this as central but neither gives it proper structural prominence. Promoting it signals its importance for the project's distinctive contribution.
- **Source priority:** Claude (semantic entropy, abstention survey, three-tier classification) layered with GEM (Jungian Shadow, Predict-Calibrate, "confidence scores and blind spots")
- **Key deliverable within section:** The three-tier (actually four-tier) epistemic classification framework: (1) factual/historical, (2) scholarly consensus, (3) interpretive/confessional, (4) matters of faith → full deferral
- **[C] material:** TBD
- **Estimated length:** 1,500–2,000 words

### Section 4: Computational Approaches to Religious and Legal Texts
- **Source priority:** Claude is substantially stronger (Latin BERT, LaBERTa, LatinPipe, CREMMA, eFontes domain adaptation problem, DISSINET, PASSIM, eScripta)
- **Unique GEM material to preserve:** CRF vs. Transformer narrative (cleaned up for precision); GNORM 3D visualization description; UbiQuity / intertextuality section; "last mile" framing for HTR limitations
- **Unique Claude material to preserve:** Research groups table; medieval Latin domain adaptation as unsolved problem; Waxman Talmud graph database; priority readings
- **[C] material:** TBD
- **Estimated length:** 2,500–3,000 words

### Section 5: Philosophy of AI and Hermeneutics
- **Source priority:** Both strong from different angles — merge
- **Claude backbone:** Scholarly genealogy (Capurro → Romele/Severo/Furia → Hornby → Picca et al. → Henrickson/Meroño-Peñuela); digital theology (Phillips/CODEC); techno-gnosticism grounded in Valčo's own work
- **GEM tissue to graft:** Gadamer "horizon" accessibility; Ricoeur faith/suspicion theological application; "Pixelated Text" and crisis of authority; "Generator of Diversity" (Donati); "Relational Realism" as antidote
- **Key move:** The five under-theorised gaps (from Claude's Section 3 conclusion) belong here as "the contribution space defined"
- **[C] material:** TBD
- **Estimated length:** 2,500–3,000 words

### Section 6: Human-Centred AI Design — Christian Personalism and Technical Standards
- **Source priority:** Claude is substantially richer
- **Claude backbone:** AI²L reframing (Natarajan et al.); Huang et al. autonomy levels (L1–L5); Shneiderman HCAI; ExtracTable and AutoLit HITL examples; TRUST framework (McGrath et al.); IEEE/CST mapping; Rome Call; Floridi/Cowls explicability; the relational ontology → architecture translation table; MCP specification and adoption
- **GEM tissue to graft:** "Relational Ontology for the AI" metaphor for MCP; "Subjectivity of Work" (John Paul II); "Graduated Autonomy" accessibility
- **Key deliverable within section:** Domain-specific autonomy mapping for religious studies tasks (L1–L4 by task type)
- **[C] material:** TBD
- **Estimated length:** 2,500–3,000 words

### Section 7: European Research Infrastructure (2026 Status)
- **Source priority:** GEM for V4 comparison; Claude for ITSERR/RESILIENCE detail
- **Unique GEM material (essential):** Table 2 (European Digital Religious Infrastructure Comparison); V4 country profiles (Polona, Manuscriptorium, Slovakiana, MaNDA); CLARIN/DARIAH interface description
- **Unique Claude material:** RESILIENCE ESFRI detail; ITSERR work package granularity; Tóth (2020) on V4 digitization
- **NEW subsection needed:** "Slovakia's Position and the ELTF Opportunity" — connecting the infrastructure landscape to the RESILIENCE Observer status strategy and Bologna General Assembly (May 2026)
- **[C] material:** TBD
- **Estimated length:** 1,500–2,000 words

### Section 8: Operational Roadmap for the TNA Fellowship [NEW — NOT IN EITHER SOURCE]
- **Rationale:** This transforms the synthesis from a reference document into a working tool. Neither report contains this; both point toward it.
- **Content:** Prototype architecture decisions that follow from the research; priority reading schedule mapped to the 2.5-week window; GNORM integration pathway; deliverable timeline; post-fellowship publication strategy
- **Note:** Write initial version now; update after Arianna meeting (Feb 12) and seminar (Feb 25) with real specifics
- **[C] material:** TBD
- **Estimated length:** 1,500–2,000 words

### Section 9: Conclusion — Towards a Relational AI for Theology
- **Source priority:** Claude's five-gap convergence analysis as backbone; GEM's concluding "clear path forward" points as accessible framing
- **Key elements:** Five convergence gaps; recommended prototype architecture specification; target publication venues and timeline; broader strategic framing (RESILIENCE, Slovakia positioning)
- **[C] material:** TBD
- **Estimated length:** 800–1,000 words

### Consolidated Bibliography
- **Task:** Deduplicate all citations across all three reports; standardise format (Author, Year, Title, Journal/Venue, DOI where available); flag citations that lack DOIs for verification
- **Estimated count:** ~150–160 unique sources after deduplication (may increase with [C])

---

## 4. TARGETED SEARCHES NEEDED

### Search 1: Recent (Jan–Feb 2026) developments in agentic AI for humanities ✅ COMPLETED
- **Completed:** February 13, 2026 (Session 3)
- **Result:** Confirmed Gap 1 — no peer-reviewed work applies agentic AI to humanities or theological research
- **Sources found:** Li & Wu (2025) on prompt engineering dilemma; Jenkins et al. (2025) on "epistemic friction" in qualitative coding

### Search 2: Protestant Reformation-era corpus computational analysis
- **Rationale:** Both reports identify this as a gap; Stöckel corpus is the actual test case; need to know what DOES exist
- **Query focus:** Reformation Latin NLP; 16th-century corpus digital analysis; Protestant theological texts computational; Leonard Stöckel digital
- **Tool:** Scholar Gateway + web search
- **When:** Before writing Section 4
- **Status:** Not yet run

### Search 3: Epistemic modesty for interpretive (vs. factual) AI tasks ✅ COMPLETED
- **Completed:** February 13, 2026 (Session 3)
- **Result:** No peer-reviewed work addresses epistemic modesty for interpretive domains specifically — strengthens novelty claim
- **Sources found:** Jenkins et al. (2025) "epistemic friction" concept as closest analogue

### Search 4: Christian personalism translated into AI architecture ✅ COMPLETED
- **Completed:** February 13, 2026 (Session 2)
- **Sources found:** Laracy et al. (2025) IEEE/CST framework; Fioravante & Vaccaro (2025) personalism in GAI; Tuppal et al. (2025) relational ontology hermeneutics

---

## 5. BUILD SEQUENCE (phased)

### Phase 1: Strategy & Outline ✅ COMPLETE
- [x] Assess both source documents ([A] and [B])
- [x] Identify overlap, tensions, unique material
- [x] Define integrated structure
- [x] Create this strategy document
- [x] Build detailed section-by-section outline with specific paragraph-level integration notes
  - File: `integrated_report_detailed_outline.md` (631 lines, synced to GitHub)

### Phase 1b: Integrate Third Source [C] ← CURRENT STEP
- [ ] Deep read Chat report
- [ ] Assess unique material, stronger treatments, new citations, tensions
- [ ] Update `integrated_report_detailed_outline.md` with [C] tags and material
- [ ] Update bibliography assembly notes
- **Prompt prepared:** `PROMPT_integrate_chat_report.md`

### Phase 2: Core Sections (Sections 2, 3, 6) — Highest priority
- **Why these first:** Most directly relevant to prototype work and Arianna meeting
- [x] Run Search 1 (recent agentic AI for humanities) — confirmed gap
- [x] Run Search 3 (epistemic modesty for interpretive tasks) — confirmed gap
- [x] Run Search 4 (personalism → AI architecture) — 3 new sources found
- [ ] Draft Section 2 (Agent Architectures)
- [ ] Draft Section 3 (Epistemic Modesty)
- [ ] Draft Section 6 (Human-Centred Design / Personalism)

### Phase 3: Scholarly Backbone (Sections 4, 5)
- [ ] Run Search 2 (Reformation-era computational work)
- [ ] Draft Section 4 (Computational Approaches to Religious Texts)
- [ ] Draft Section 5 (Philosophy of AI and Hermeneutics)

### Phase 4: Framing & Context (Sections 1, 7, 9)
- [ ] Draft Section 1 (Introduction)
- [ ] Draft Section 7 (European Infrastructure) — includes new Slovakia subsection
- [ ] Draft Section 9 (Conclusion)

### Phase 5: Operational & Assembly
- [ ] Draft Section 8 (Operational Roadmap) — after Arianna meeting data
- [ ] Compile consolidated bibliography
- [ ] Full integration pass — voice, flow, cross-references
- [ ] Revision pass — precision, citation verification, redundancy removal

---

## 6. QUALITY STANDARDS

### Voice
- Use Michal's characteristic academic voice (see userPreferences)
- Rhetorical presentation: build toward conclusions rather than announcing thesis upfront
- Vary sentence length; allow parenthetical asides and self-corrections
- No AI clichés ("delve," "navigate," "leverage," "tapestry," "in the ever-evolving landscape")
- No formal connectors ("Furthermore," "Moreover," "It is important to note")

### Citation Standards
- Full bibliographic entries: Author(s), Year, "Title," *Journal/Venue* Volume(Issue): Pages. DOI.
- In-text: (Author, Year) or Author (Year) — not superscript numbers
- Flag any citation that lacks a verifiable DOI or stable URL for later verification
- Prefer peer-reviewed sources; blog posts and web pages only where content is unique and verifiable

### Source Tagging
- `[A]` = Claude Report
- `[B]` = GEM (Gemini) Report
- `[C]` = Chat (ChatGPT) Report
- `[NEW]` = from targeted searches (Feb 13, 2026)

### Architectural Coherence
- Every section should connect back to the five-gap analysis (the contribution space)
- Technical recommendations must trace to philosophical principles (the personalism → architecture bridge)
- The document should be usable both as a standalone reference AND as the foundation for specific deliverables (working paper, presentations, journal articles)

---

## 7. SESSION HANDOFF PROTOCOL

**At the start of each new session working on this project:**
1. Claude reads this strategy document from PKB (or filesystem copy)
2. Check the "Status" line at top and the Phase 1–5 checklist for current position
3. Review any notes in Section 8 below for session-specific context

**At the end of each session:**
1. Update the checklist in Section 5 (check off completed items)
2. Add session notes to Section 8 below
3. Update the "Last updated" date and "Status" line
4. Sync filesystem copy to GitHub: `docs\resources\integrated_report_strategy.md`

---

## 8. SESSION LOG

### Session 1 — February 10, 2026
- **What happened:** Assessed both source documents ([A] and [B]) in detail via PKB search. Identified overlap (~40%), tensions (4 specific), unique material per source. Defined 9-section integrated structure. Created this strategy document.
- **Decisions made:** Claude report structure = skeleton; GEM report = grafted tissue. Two targeted searches needed. Build sequence: core technical sections first (2, 3, 6), then scholarly backbone (4, 5), then framing (1, 7, 9), then operational (8).
- **Next session should:** Build the detailed paragraph-level outline.

### Session 2 — February 11, 2026
- **What happened:** Built the detailed section-by-section outline (`integrated_report_detailed_outline.md`, 622 lines). Completed Scholar Gateway search for personalism → AI architecture.
- **Sources found:** Laracy et al. (2025) IEEE/CST framework; Fioravante & Vaccaro (2025) personalism in GAI deployment.
- **Decisions made:** Outline follows 9-section structure with paragraph-level integration notes tagged [A]/[B]. Bibliography assembly notes included as Section 10.

### Session 3 — February 13, 2026
- **What happened:** Completed four remaining tasks from Session 2 handoff:
  1. Updated §6.3.1 with Laracy et al. and Fioravante & Vaccaro citations
  2. Added 4 new sources to bibliography assembly notes
  3. Ran Scholar Gateway searches: (a) epistemic modesty for interpretive tasks — confirmed gap, found Jenkins et al. (2025) "epistemic friction"; (b) agentic AI for humanities — confirmed gap, no peer-reviewed work exists
  4. Copied outline to GitHub (`docs\resources\integrated_report_detailed_outline.md`)
- **Sources added (6 total this session):**
  - Laracy et al. (2025) — IEEE/CST framework
  - Fioravante & Vaccaro (2025) — Personalism in GAI deployment (DOI: 10.1007/s41463-024-00193-9)
  - Tuppal et al. (2025) — Relational ontology hermeneutics (DOI: 10.1111/scs.70097)
  - Li & Wu (2025) — Prompt engineering dilemma (DOI: 10.1002/sdr.70008)
  - Jenkins et al. (2025) — Epistemic friction in qualitative analysis (DOI: 10.1002/jls.70014)
  - Search notes documenting gap confirmation
- **New task identified:** Integrate third source [C] = Chat Report (436KB .docx) before Phase 2 drafting
- **Prompt prepared:** `PROMPT_integrate_chat_report.md` saved to Resources folder
- **Updated this strategy document** with [C] references, new Phase 1b, completed search results, session log
- **Next session should:** Execute PROMPT_integrate_chat_report.md — deep read [C], assess, update outline, then proceed to Phase 2 drafting

### Session 4 — February 13, 2026 (later)
- **What happened:** Created `pipeline_technical_reference.md` (~230 lines) for Claude Project PKB. Read CIC_annotation Deep Dive (567 lines), workflow diagram (358 lines), epistemic modesty framework, and confirmed source code structure. Condensed into quick-lookup reference card covering: 6-layer pipeline architecture, BIOES format, entity types (current 4 + proposed 7), CRF feature engineering, source tracking → epistemological classification mapping, dependencies, adaptation gaps, and open questions.
- **Files created:** `docs/resources/pipeline_technical_reference.md`
- **HUB updates:** Current Status updated; PKB Contents table updated (removed "planned" marker).
- **Next session should:** Upload `pipeline_technical_reference.md` to Claude Project PKB. Then resume synthesis work — execute PROMPT_integrate_chat_report.md.

### Session 5 — February 14, 2026
- **What happened:** Deep read analysis of GEM and CHAT reports (~782 + ~893 lines) against all PKB documents. Produced `deep_read_GEM_CHAT_analysis.md` (saved to `docs/resources/` and uploaded to PKB). Identified 8 surgical additions for live reference docs, confirmed ~70% overlap with existing knowledge, found no corrections needed. Three genuinely new findings: ATON Framework identification (unconfirmed), Omeka S/IIIF integration architecture, Pavone & Imperia Talmud cross-domain precedent.
- **Files created:** `docs/resources/deep_read_GEM_CHAT_analysis.md`, `docs/resources/PROMPT_apply_deep_read_additions.md`
- **PKB updated:** `deep_read_GEM_CHAT_analysis.md` uploaded to PKB by user.
- **HUB updates:** Current Status, Decision Log updated.
- **Session froze** before applying edits to live reference docs. Handoff prompt written.
- **Next session should:** Execute `PROMPT_apply_deep_read_additions.md` — apply 8 edits to `pipeline_technical_reference.md` and `workflow_diagram.md`. Then resume synthesis — either execute PROMPT_integrate_chat_report.md or begin Phase 2 drafting.

---

## 9. FILE LOCATIONS

| File | Path |
|------|------|
| **This strategy document** | `C:\Users\valco\...\Resources\integrated_report_strategy.md` |
| **Detailed outline** | `C:\Users\valco\...\Resources\integrated_report_detailed_outline.md` |
| **[A] Claude Report** | PKB: `Ethically-Grounded_AI_Agents_for_Religious_Studies_...md` |
| **[B] GEM Report** | `C:\Users\valco\...\Resources\AI Agents for Religious Studies (GEM) Report.docx` |
| **[C] Chat Report** | `C:\Users\valco\...\Resources\Report (CHAT) - Towards an Ethically-Grounded AI Research Assistant.docx` |
| **Integration prompt** | `C:\Users\valco\...\Resources\PROMPT_integrate_chat_report.md` |
| **GitHub outline** | `C:\Users\valco\...\GitHub\ITSERR-RESILIENCE-Project\docs\resources\integrated_report_detailed_outline.md` |

*(All paths abbreviated; full prefix: `C:\Users\valco\OneDrive\Documents\04 Projekty\2025 ITSERR - Resilience Project\Resources\`)*

---

*This document should be kept in sync between the Claude Project Knowledge Base and the filesystem copy.*

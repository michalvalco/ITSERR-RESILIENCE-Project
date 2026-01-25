# ITSERR/RESILIENCE Fellowship Milestones

## Overview

This document tracks deliverables and milestones for the TNA Fellowship at University of Palermo / CNR-ISTI (February 10–27, 2026).

---

## Phase 1: Foundation Building (Now → Feb 9, 2026)

**Goal:** Arrive at Palermo with sufficient preparation to maximize fellowship time.

### 1A. Core Preparation

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Complete bibliography (15-20 sources) | Feb 2 | ☐ Pending | Annotated, organized by theme |
| Draft epistemic_modesty_framework.md v1 | Feb 5 | ☐ Pending | Core theoretical contribution |
| Draft system_design.md | Feb 5 | ☐ Pending | Component diagram + data flow |
| Draft working paper outline (Sections 0-6) | Feb 7 | ☐ Pending | Skeletal structure acceptable |
| Review GNORM codebase | Feb 9 | ☑ Complete | Jan 25: Full analysis in stockel_annotation/scripts/ |
| Set up dev environment | Feb 9 | ☑ Complete | Jan 25: GNORM deps installed (cassis, crfsuite) |
| Prepare questions for WP3 team | Feb 9 | ☑ Complete | Jan 25: gnorm_briefing_questions.md (16 sections, 6 Stöckel-specific) |
| Read ITSERR WP documentation | Feb 9 | ☐ Pending | Surface familiarity WP4-8 |

### 1B. Stöckel Corpus Preparation (Pilot Study)

**Detailed tracking:** See `03_prototype/stockel_annotation/PROGRESS.md`

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Clone GNORM repo & run test annotation | Feb 2 | ☑ Complete | Jan 25: Pipeline analyzed, WebAnno TSV format verified |
| Download Zenodo dataset & examine structure | Feb 2 | ☑ Complete | Jan 25: 186 docs total (39 expert-annotated with 18,425 tokens, 462 unique refs) |
| Select 2-3 Stöckel texts for pilot | Feb 4 | ☑ Complete | Jan 25: De Peccato Originis, De Iustificatione, De Lege et Evangelio |
| Create cleaned digital versions | Feb 6 | ☐ Pending | UTF-8 plain text, normalized |
| Begin manual annotation (100+ refs) | Feb 9 | ☐ Pending | Using INCEpTION |
| Document annotation schema decisions | Feb 9 | ☐ Pending | Adaptation from GNORM schema |
| Draft email to Arianna (pilot proposal) | Feb 7 | ☑ Complete | Jan 25: Drafted in 05_admin/correspondence/ |

### Phase 1 Success Criteria
- [ ] Can articulate the epistemic modesty framework in 5 minutes
- [ ] Have concrete questions for GNORM technical briefing
- [ ] Know where the prototype will integrate with existing tools
- [ ] **Stöckel pilot:** Have 2-3 cleaned texts with 100+ manual annotations
- [x] **Stöckel pilot:** Can run GNORM pipeline on test data (verified Jan 25)

---

## Phase 2: Research & Orientation (Week 1: Feb 10–16)

**Goal:** Technical briefings + literature deepening + framework refinement.

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Technical briefing with GNORM team | Feb 11-12 | ☐ Pending | Scheduled with Dr. Pavone |
| Refine epistemic_modesty_framework.md | Feb 14 | ☐ Pending | Incorporate GNORM insights |
| Create literature notes (5-7 sources) | Feb 15 | ☐ Pending | Detailed annotations |
| Document GNORM integration patterns | Feb 16 | ☐ Pending | code_notes/gnorm_patterns.md |
| Draft concept_map.md | Feb 16 | ☐ Pending | Visual thinking aid |
| Draft Sections 1-2 of working paper | Feb 16 | ☐ Pending | Introduction + Background |

### Phase 2 Success Criteria
- [ ] Understand GNORM CRF annotation pipeline
- [ ] Have clear integration points documented
- [ ] Working paper Sections 1-2 have substantive content

---

## Phase 3: Development Sprint (Week 2: Feb 17–23)

**Goal:** Prototype implementation + writing acceleration.

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Implement narrative memory system | Feb 20 | ☐ Pending | Core innovation #1 |
| Implement epistemic indicators | Feb 21 | ☐ Pending | Core innovation #2 |
| Draft Sections 3-4 of working paper | Feb 21 | ☐ Pending | Framework + Implementation |
| Document design decisions | Feb 22 | ☐ Pending | Philosophical-technical mappings |
| Implement tool-calling patterns | Feb 23 | ☐ Pending | Core innovation #3 |
| Create integration examples | Feb 23 | ☐ Pending | GNORM/T-ReS demonstrations |

### Phase 3 Success Criteria
- [ ] All three core innovations have working implementations
- [ ] Working paper Sections 1-4 complete
- [ ] At least 5 philosophical-technical mappings documented

---

## Phase 4: Completion & Delivery (Week 3: Feb 24–27)

**Goal:** Finalize deliverables. Only 4 days—protect this time.

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Finalize presentation slides | Feb 25 | ☐ Pending | Due Feb 26 for review |
| Complete Sections 5-6 of working paper | Feb 26 | ☐ Pending | Discussion + Conclusion |
| Create demo script | Feb 26 | ☐ Pending | Reproducible demonstration |
| Deliver consortium presentation | Feb 27 | ☐ Pending | 40-minute slot |
| Draft blog post outline | Feb 27 | ☐ Pending | Full draft can wait |

### Phase 4 Success Criteria
- [ ] Presentation delivered successfully
- [ ] Working paper complete (all 7 sections, 5,000+ words)
- [ ] Demo runs without errors
- [ ] Blog post outline captured

---

## Phase 5: Post-Fellowship (March 2026)

**Goal:** Consolidation and publication.

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Complete blog post | Mar 15 | ☐ Pending | 800-1200 words |
| Submit to ITSERR website | Mar 20 | ☐ Pending | Coordinate with communications |
| Enhancement suggestions | Mar 31 | ☐ Pending | GitHub Projects, CI/CD if time |

---

## Key Deliverables Summary

| Deliverable | Target Completion | Word Count / Scope |
|-------------|-------------------|--------------------|
| Working Paper | Feb 27 | 5,000+ words, 7 sections |
| Prototype | Feb 27 | 3 core innovations working |
| Presentation | Feb 27 | 40 minutes |
| Blog Post | Mar 15 | 800-1200 words |
| Code Annotations | Feb 27 | ≥5 philosophical-technical mappings |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| GNORM codebase more complex than expected | Medium | High | Front-load review in Phase 1 |
| Limited deep-thinking time during Week 1 | High | Medium | Draft framework before arrival |
| Technical environment issues | Low | High | Set up and test before fellowship |
| Presentation overruns 40 minutes | Medium | Low | Practice run on Feb 26 |
| Integration with WP tools delayed | Medium | Medium | Document integration points even if not implemented |

---

## Daily Log Template

Use this template for daily progress tracking:

```markdown
## [Date]

### Completed Today
-

### In Progress
-

### Blocked / Questions
-

### Tomorrow's Priority
-
```

---

*Last updated: January 25, 2026*

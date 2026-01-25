# Email Draft: Pilot Study Proposal to Dr. Arianna Maria Pavone

**To:** Dr. Arianna Maria Pavone (WP3 Coordinator, University of Palermo)
**Subject:** Stöckel Corpus Pilot Study Proposal — GNORM Adaptation for Reformation Theology
**Date:** Draft prepared January 25, 2026
**Status:** DRAFT — Review before sending

---

## Email Text

Dear Dr. Pavone,

I hope this message finds you well. As my Transnational Access Fellowship approaches (February 10-27), I wanted to share my preparatory work and propose a concrete pilot study for our collaboration.

### Background: The Opportunity

Following my review of the GNORM codebase and Zenodo dataset, I'm struck by the potential for adapting your CRF-based annotation approach to my primary research corpus: the theological works of Leonard Stöckel (1510-1560), a Slovak Lutheran humanist whose writings exhibit citation patterns structurally similar to medieval gloss traditions.

### Proposed Pilot Study

I propose testing GNORM's transferability by annotating 3 chapters from Stöckel's *Annotationes in Philippi Melanchthonis Locos Praecipuos Theologicos* (1561):

1. **De Peccato Originis** (On Original Sin) — Extensive Augustinian citations
2. **De Iustificatione** (On Justification) — Dense biblical and patristic references
3. **De Lege et Evangelio** (On Law and Gospel) — Foundational Lutheran hermeneutics

These chapters were selected based on expected citation density (125-180 references total) and diversity of citation types: biblical, patristic, classical, and contemporary Reformation sources.

### Why This Matters

This pilot would address a significant gap: no automated annotation system currently exists for Reformation-era theological commentaries. Success would demonstrate GNORM's applicability beyond medieval canon law, potentially opening new research communities to ITSERR's tools.

Key differences we'd need to address:
- Biblical citation formats (Book Chapter:Verse) vs. legal citation formats
- Patristic author abbreviations (Aug., Chrys., Hieron.) vs. legal source abbreviations
- Mixed Latin-German passages in 16th-century texts

### My Preparation

Before arriving in Palermo, I will have:
- Cleaned digital text of the selected chapters (UTF-8, normalized)
- 100+ manually annotated references using INCEpTION
- Documented annotation schema decisions
- Technical questions for pipeline adaptation (attached as briefing document)

### Proposed Collaboration

During the fellowship, I would welcome the opportunity to:
1. Review annotation schema decisions with your team
2. Run initial experiments using GNORM's CRF approach
3. Discuss feature adaptations for theological citation formats
4. Explore potential joint publication on cross-domain transfer

If the pilot proves successful, this could become a case study for GNORM's generalizability—demonstrating that the architectural choices your team made for canon law extend meaningfully to adjacent domains.

### Next Steps

I would be grateful for any feedback on this proposal before my arrival. In particular:
- Does this scope seem feasible for a 2.5-week fellowship?
- Are there specific aspects of the pipeline you'd recommend I focus on?
- Would the team be interested in a formal collaboration or co-authored publication?

I have prepared a detailed technical questions document that I'll bring to our briefing sessions on February 11-12.

Thank you for your guidance and for making this fellowship opportunity possible. I look forward to productive discussions in Palermo.

With warm regards,

Michal Valčo
Comenius University in Bratislava
Faculty of Arts

---

## Attachments to Include

1. `CHAPTER_SELECTION.md` — Full rationale for pilot text selection
2. `gnorm_briefing_questions.md` — Technical questions document (Stöckel sections highlighted)

---

*Draft prepared: January 25, 2026*

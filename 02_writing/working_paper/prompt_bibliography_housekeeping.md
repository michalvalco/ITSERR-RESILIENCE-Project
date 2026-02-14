# Prompt: Bibliography Housekeeping and Citation Verification

**Paste this entire prompt into a fresh Claude session. The working paper draft should be in the Project Knowledge Base.**

---

## Context

I'm finalizing a ~16,000-word research synthesis (`tna_working_paper_draft.md` in PKB) targeting *AI & Society* and *Digital Scholarship in the Humanities*. An editorial pass found **ten missing bibliography entries**, **two unverified sources cited without hedging**, and **several factual items requiring verification**. These create unnecessary reviewer risk for a paper whose central argument is about epistemic modesty.

Your job is to fix all of these. Use web search to verify sources, find DOIs, and confirm factual claims. Produce two outputs: (1) a corrected bibliography block I can drop into the paper, and (2) a list of specific in-text edits keyed to section numbers.

---

## Task A: Missing Bibliography Entries

The following sources are **cited in the main text** but have **no entry in the References section**. For each one, search the web, find the correct full citation (author, year, title, venue, DOI/URL), and produce a formatted bibliography entry. If a source cannot be verified, say so explicitly — do not fabricate entries.

### A1. BiblIndex project (Lyon)
- **Cited in:** §4.2 — "The BiblIndex project at Lyon provides a comprehensive index of biblical quotations in patristic literature"
- **What to find:** The project's main publication or reference article. Likely Laurence Mellerin or the Sources Chrétiennes team at CNRS Lyon.

### A2. BLAST bioinformatics method applied to patristic text reuse
- **Cited in:** §4.2 — "BLAST, a bioinformatics sequence-alignment method, has been applied to patristic text reuse detection"
- **What to find:** The specific paper that applied BLAST to patristic/medieval text reuse. This is a methodological transfer from bioinformatics to digital humanities.

### A3. LatinPipe / EvaLatin 2024
- **Cited in:** §4.1 — "The EvaLatin 2024 competition winner, LatinPipe from ÚFAL at Charles University, Prague"
- **What to find:** The EvaLatin 2024 shared task proceedings or the LatinPipe system description paper. Authors likely include Milan Straka or ÚFAL team members.

### A4. DISSINET project (Masaryk University, Brno)
- **Cited in:** §4.1 — "The DISSINET project at Masaryk University, Brno, addresses this by applying Computer-Assisted Semantic Text Modelling (CASTEMO)"
- **What to find:** A main DISSINET publication. PI is likely David Zbíral. Look for their methodological paper on CASTEMO or medieval inquisition record analysis.

### A5. Sefaria MCP server (2025)
- **Cited in:** §4.2 and §6.4 — "Sefaria... has developed an MCP server (2025) enabling AI assistants to query authoritative texts in real time"
- **What to find:** The Sefaria MCP server announcement, GitHub repository, or blog post. This is a software release, not a journal article — cite with URL and access date.

### A6. John Henry Newman — "illative sense"
- **Cited in:** §2.3 — "what Newman called an *illative sense*, a capacity for judgment that develops through sustained, patient engagement"
- **Entry needed:** Newman, J.H. (1870). *An Essay in Aid of a Grammar of Assent*. Burns, Oates, & Co. — Verify this is the correct source for the "illative sense" concept and provide a standard citation.

### A7. Matteo Valleriani (Max Planck Institute)
- **Cited in:** §4.2 and §7.3 — "Valleriani's work at the Max Planck Institute for the History of Science" on Wittenberg print culture
- **What to find:** A specific publication by Valleriani on early modern print networks / knowledge dissemination from the MPIWG. He has several; find one that fits the "Reformation print culture diffusion patterns" context.

### A8. Pope Leo XIV — quoted statement
- **Cited in:** §6.3 — "Pope Leo XIV stated that 'access to data must not be confused with intelligence' and that AI must account for 'the well-being of the human person not only materially, but also intellectually and spiritually.'"
- **What to find:** The specific document (World Communications Day message? Address? Encyclical?) in which Pope Leo XIV made these statements. Provide title, date, and URL if available from vatican.va.

### A9. Somanunnithan (2025) — CrewAI demonstration
- **Currently:** Listed in the "Sources Requiring DOI Verification" appendix but not in the main bibliography. Cited in §2.2.
- **Action:** Search for this source. If it's grey literature (blog post, tutorial, GitHub demo) that can't be properly cited in an academic bibliography, I need to know. In that case, the in-text citation should be removed and the point reattributed or described without named attribution. If a citable source exists, add it.

### A10. AutoGen — Wu et al. (2023)
- **Currently:** *In* the bibliography but the in-text reference in §2.2 mentions "Microsoft AutoGen" by product name only, without a parenthetical citation.
- **Action:** Provide the exact in-text edit needed in §2.2 to add the citation. The bibliography entry already exists: Wu, Q., et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." arXiv:2308.08155.

---

## Task B: Orphaned Bibliography Entry

### B1. Le Duc, A. (n.d.). "Towards a Cybertheology: Theology in the Digital Milieu." SSRN: 4337184.
- Le Duc's 2026 keynote IS cited in §5.3, but this earlier SSRN preprint is in the bibliography without an in-text citation.
- **Action:** Either (a) find a natural place in §5.3 to cite it — Le Duc's "cybertheology" concept is directly relevant to the digital theology discussion — and provide the exact in-text insertion, OR (b) recommend removal from the bibliography. Option (a) is preferred if it fits naturally.

---

## Task C: Unverified Sources — Verify or Hedge

### C1. Adeboye, A., et al. (2025) — AI and indigenous African religion
- **Cited in:** §5.3 — "Adeboye et al. (2025) document that encoding oral divination verses of indigenous African religion into a binary AI model failed to capture the spiritual intent"
- **Problem:** Venue and DOI unconfirmed. Cited in the main text without any hedge.
- **Action:** Search for this paper. If found, provide full citation. If not found, provide a hedged in-text revision: something like "Recent work (Adeboye et al., 2025; venue pending confirmation) documents that..."

### C2. "AI as Interpretive Aid in Qur'anic Stylistics" (2025)
- **Cited in:** §5.3 — referenced for the *i'jaz* doctrine discussion. The bibliography notes say "Author(s), venue, and DOI unconfirmed. Not included in the bibliography pending verification."
- **Problem:** The claim about *i'jaz* and computational Qur'anic analysis appears in the main text without attribution to a verified source.
- **Action:** Search for this paper or a similar verified publication on computational approaches to Qur'anic stylistics and the *i'jaz* doctrine. If found, provide full citation. If not found, either (a) find an alternative verified source that makes a similar point about computational limits and *i'jaz*, or (b) provide revised text that attributes the *i'jaz* point to general Islamic theological scholarship rather than to an unverifiable computational study.

---

## Task D: Factual Verification

### D1. *Humanae Dignitatis* (2023)
- **Cited in:** §6.3 — "The Vatican's follow-up document *Humanae Dignitatis* (2023) expanded these principles"
- **Problem:** I could not verify a Vatican document by this exact title. The 2024 Vatican declaration on human dignity is *Dignitas Infinita*. There may also be confusion with *Dignitatis Humanae* (1965, Vatican II).
- **Action:** Search for the correct title and date. Is there a 2023 Vatican document following up on the Rome Call? If this is *Dignitas Infinita* (2024), correct the title and date. If the document doesn't exist, remove the reference and note what should replace it (if anything).

### D2. Piotrowski (2026) DOI
- **Current DOI:** `10.1007/978-3-032-08697-6_2`
- **Problem:** Springer LNCS ISBNs typically use `978-3-031-...` or `978-3-030-...`. The `032` prefix is unusual and may be a typo.
- **Action:** Verify whether this DOI resolves. If it's a typo, provide the correct DOI.

### D3. Latin BERT "92.4%" comparison
- **Cited in:** §4.1 — "the GNORM pipeline's CRF achieves 97.8% accuracy on legal reference annotation in the *Liber Extra*, compared to Latin BERT's 92.4% on the same task"
- **Problem:** The 92.4% figure has no citation. It may be from the Esuli, Imperia & Puccetti (2025) paper itself (as a comparison they ran) or from a different benchmark entirely.
- **Action:** Search for the source of this comparison. If it's from the CIC_annotation paper, note that. If it's from a different benchmark (i.e., Latin BERT's score on a *different* task), flag it and provide revised text that avoids a misleading head-to-head comparison.

### D4. Manuscriptorium statistics
- **Cited in:** §7.2 — "over 360,000 descriptive records, 33 million digitised pages, and 130,000 digitised documents from more than 180 institutions in approximately twenty countries"
- **Problem:** A different source document gives different figures (400K records, 110K documents, 139 partners, 24 countries). These likely reflect different access dates.
- **Action:** Check manuscriptorium.com for current statistics and provide the correct figures with an access date.

---

## Task E: New Addition

### E1. Puccetti, G., Imperia, R., & Esuli, A. (2024). "GNORM Overview." *ERCIM News* 141.

- **Action 1:** Search for this article, confirm publication details, and find a URL or DOI.
- **Action 2:** Add it to the bibliography.
- **Action 3:** Find the most natural place in the paper for a passing reference. The best candidate is §4.3 (GNORM and 3D Visualisation), where the GNORM project is introduced. The reference should be woven in naturally — not a direct quote, just acknowledgment that the project has been described in the literature. For example, something like adding "(Puccetti, Imperia, & Esuli, 2024)" alongside the existing Esuli, Imperia, & Puccetti (2025) reference, or noting that the GNORM project has been presented in overview form. Provide the exact in-text edit with enough surrounding context that I can locate where it goes.

---

## Output Format

Produce three sections:

### 1. New and Corrected Bibliography Entries
For each item (A1–A10, E1), provide the formatted entry ready to paste into the References section. Use the same citation style as the existing bibliography (author-date, journal in italics, DOI where available). Mark any entries you could NOT verify with **[UNVERIFIED — recommend removal or hedging]**.

### 2. In-Text Edits
For each edit needed (B1, C1, C2, D1–D4, E1 insertion, A10 citation addition, and any other fixes), provide:
- **Section:** §X.Y
- **Current text:** (quote enough surrounding context to locate it — 1–2 sentences)
- **Revised text:** (the replacement, with changes marked in **bold**)
- **Reason:** (one sentence)

### 3. Items That Could Not Be Resolved
List anything you couldn't verify or find, with a recommendation for each (remove? hedge? defer to author?).

---

## Constraints

- **Do NOT rewrite sections.** Provide surgical edits only.
- **Do NOT invent citations.** If you can't find a source, say so.
- **Prefer DOIs over URLs** where both exist.
- **For grey literature** (blog posts, GitHub repos, software announcements), use standard formats: Author/Organization. (Year). "Title." Retrieved [date] from [URL].
- **Be explicit about confidence.** If you found something that *might* be the right source but aren't certain, say "likely match" and flag for my verification.

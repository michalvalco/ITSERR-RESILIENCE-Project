# Editorial Pass Report: TNA Working Paper Draft

**Paper:** "Designing Ethically-Grounded AI Agents for Religious Studies Research: A Comprehensive Research Synthesis"  
**Author:** Prof. Michal Valčo  
**Reviewer:** Claude (editorial analysis, February 14, 2026)  
**Target venues:** *AI & Society* / *Digital Scholarship in the Humanities*

---

## Pass 1: Structural Integrity

### Issues Found

1. **[§1 Introduction, ¶5]** — The five-gap enumeration in the Introduction is the structural spine of the entire paper, and it works well. However, the numbering scheme shifts between the Introduction and §9 (Conclusion). In §1.4 (the fifth paragraph of the Introduction), the five gaps are listed as a flowing paragraph with embedded numbering. In §9, they are re-enumerated with "First... Second... Third... Fourth... Fifth..." phrasing. The *order* is identical in both places (agentic gap, personalism gap, Protestant gap, epistemic modesty gap, agentic orchestration gap), which is good. But there's a subtle drift: in §1, the fifth gap is framed as "ITSERR's emerging tools await agentic orchestration" (emphasizing the tools), while in §9 it is framed around the Model Context Protocol specifically. These are compatible but not identical framings.  
   **Recommendation:** Align the §9 framing of Gap 5 more precisely with §1. The MCP detail belongs in the development of the point, not in its statement. A single consistent sentence for each gap's "headline" across §1, §9, and wherever they recur (§2.4, §3.1, §4.3 closing, §5.4, §7.3) would tighten the spine considerably. Trivial fix but high structural payoff.

2. **[§2.2 — Framework Comparison]** — This section runs approximately 2,800 words, making it the longest subsection in the paper. The comparison table is well-constructed, but the prose *before* the table essentially narrates what the table then presents again. The LangGraph description alone is ~600 words; the Stöckel hypothetical example embedded within it is vivid but adds length. The CrewAI "Philologist Agent / Systematic Theologian Agent" role-play, while illustrative, could be compressed. The AutoGen section is the most concise of the three and works well.  
   **Recommendation:** Trim §2.2 to ~2,000 words. Specifically: compress the LangGraph prose to focus on the two features that matter most (graph-as-hermeneutical-circle and state-as-interpretation-locus); reduce the CrewAI discussion by cutting the extended role-naming conceit; let the comparison table do more of the heavy lifting. The final "theological suitability" row and the paragraph defending it are the strongest part — protect those. Estimated effort: medium.

3. **[§7 — European Research Infrastructure]** — At ~2,400 words, this section carries more descriptive weight than argumentative weight. §7.1 and §7.2 read like a well-researched landscape survey but could be tightened. The CEE digitization catalogue in §7.2 (Manuscriptorium stats, Hungaricana, Cantus.sk, FamilySearch, etc.) is thorough but largely reportorial — it documents what exists without always connecting each item back to the paper's argument. The strongest part is §7.3, where the five infrastructure gaps are identified. That's where the argumentative energy is.  
   **Recommendation:** Cut §7.1 by ~200 words (the ITSERR work-package list can be compressed — the reader doesn't need every WP described). Cut §7.2 by ~300 words by being more selective: keep Manuscriptorium (flagship), the Slovak specifics (directly relevant), and the Fragmentarium project, but compress the Hungarian and Polish material to two sentences each. This lets §7.3 land with more force. Estimated effort: small–medium.

4. **[§8 — Operational Roadmap, Tense Issues]** — The fellowship timeline (Feb 10–27) means that by the time you're reading this, Week 1 is past and Week 2 is underway. §8.2 uses past tense for Week 1 ("established the pivot," "was assembled during this week") — good. But Week 2 is written in a mix: "Working paper draft: the personalist foundations..." reads as a task description (present/imperative), not as a report. "The workflow diagram... was refined collaboratively" is past tense, suggesting it's done. "Implementation work: concrete tool definitions, MCP integration stubs, testing against GNORM API endpoints if available from the WP3 team" reads as future-conditional.  
   **Recommendation:** Decide: is §8.2 a retrospective account of what was done (report format) or a plan for what will be done (roadmap format)? For a publication, the former is stronger — it tells readers what *was* accomplished, not what was *hoped*. Rewrite Week 2 and Days 13–17 in past tense once the fellowship concludes, converting plans into results. Flag items that weren't completed as "deferred to post-fellowship." Estimated effort: small (but must wait until after Feb 27).

5. **[§9 — Conclusion]** — The conclusion is *almost* a synthesis rather than a summary, but it doesn't quite get there. It re-enumerates the five gaps (good — closure), restates the recommended architecture (good — specificity), and ends with a rhetorically strong final paragraph about "an agent that respects the sacredness of the text." But what's missing is the *convergence claim* stated explicitly: why do these five gaps, together, produce something that none of them individually could? The Introduction promises that "five distinct literature gaps converge at a point that, taken together, defines a genuinely novel contribution space," but the Conclusion doesn't fully deliver on this by showing *how* they converge — how the personalism gap (Gap 2) shapes the solution to the epistemic modesty gap (Gap 4), how the Protestant corpus gap (Gap 3) provides the test case for the agentic gap (Gap 1), etc.  
   **Recommendation:** Add one paragraph between the five-gap enumeration and the architecture recommendation that explicitly maps the convergence. Something like: "These gaps are not additive but synergistic. The absence of epistemic modesty frameworks for interpretive domains (Gap 4) cannot be addressed without the personalist anthropology (Gap 2) that motivates the distinction between factual and interpretive claims. The Protestant corpus gap (Gap 3) provides not merely a test case but a *calibration context* for the epistemic classification — one where confessional diversity makes the interpretive tiers empirically testable. And ITSERR's standalone tools (Gap 5) cannot be meaningfully orchestrated (Gap 1) without the design philosophy that determines *which* tools should be consulted for *which* kinds of questions." This is the paper's highest-impact structural improvement. Estimated effort: medium.

### No Issues (sections that passed clean)

- §1 Introduction (strong opening, clear scope, effective five-gap preview)
- §3 Epistemic Modesty (well-structured, four-tier framework clearly presented)
- §4.3 GNORM and 3D Visualisation (crisp, technically grounded)
- §6.2 Graduated Autonomy mapping (the table is persuasive)


---

## Pass 2: Argumentative Quality

### Issues Found

1. **[§1, ¶3]** — The claim that an AI agent introduces "a *third horizon*" (beyond text-horizon and interpreter-horizon) is philosophically ambitious and potentially the paper's most memorable conceptual contribution. But it's asserted without development. What does it mean for the training distribution to constitute a "horizon"? Gadamer's horizons are historically constituted — they carry tradition. A training distribution carries statistical regularities. Calling both "horizons" risks equivocation. The paragraph acknowledges this ("It does not have *tradition* in Gadamer's sense") but then moves on without resolving the tension.  
   **Recommendation:** Either develop the "third horizon" concept into a sustained argument (which would require ~300 additional words and engagement with Gadamer's specific criteria for what constitutes a horizon) or soften the claim to "quasi-horizon" or "pseudo-horizon" with explicit acknowledgment that the analogy is limited. The former is more interesting; the latter is safer. Estimated effort: small (softening) to medium (developing).

2. **[§2.1, ¶1]** — Kommers et al. (2025) is described as having "thirty-four additional co-authors." Source A says "37 co-authors" total. The paper says "thirty-four additional" plus the named authors (Kommers, Ahnert, Antoniak), which would be 37 total. This is consistent, but the phrasing is awkward — counting "additional" authors draws attention to itself. More importantly, the number of co-authors isn't argumentatively relevant.  
   **Recommendation:** Simplify to "Kommers, Ahnert, Antoniak, and colleagues from major digital humanities centres" or similar. The authority of the work comes from the Turing Institute affiliation, not the author count. Trivial fix.

3. **[§2.2]** — The claim that LangGraph's state object is "the *locus* of the hermeneutical act" is bold and interesting. But the argument supporting it is illustrative (the Stöckel/Augustine example) rather than demonstrative. The example shows that state *accumulates* interpretive findings, but accumulation is not the same as hermeneutics. A filing cabinet also accumulates findings. The distinctive claim — that the graph structure *models* the hermeneutical circle — needs the additional step of showing that the iterative graph traversal (returning to earlier nodes in light of later findings) is architecturally analogous to the hermeneutical circle's reciprocal movement. This step is gestured at but not completed.  
   **Recommendation:** Add 2–3 sentences after the Stöckel example explicitly connecting iterative graph traversal to the hermeneutical circle's structure. The point isn't that information accumulates (any database does that) but that later findings can trigger re-traversal of earlier nodes, updating prior interpretations — and that this re-traversal is *built into the architecture*, not an afterthought. Estimated effort: small.

4. **[§3.2 — Four-Tier Classification]** — The four tiers are well-motivated and clearly distinguished. The framework is the paper's most distinctive technical contribution. Two argumentative concerns, however:

   (a) **The boundary between Tier 2 and Tier 3 is underspecified.** When does "scholarly consensus with acknowledged disagreement" (Tier 2) shade into "multiple valid traditions" (Tier 3)? The Markan priority example (Tier 2) seems to involve a straightforward empirical question with a dominant answer. But what about "Paul wrote Ephesians" — where scholarly opinion is divided roughly 50/50? Is that Tier 2 or Tier 3? The classification needs a decision rule for borderline cases.

   (b) **Tier 4's deferral mechanism needs more precision.** The paper says the agent "refuses to generate an answer" at Tier 4. But what triggers the refusal? If the agent encounters the question "What does this text mean for the Christian life?" in a user query, how does it *recognize* that this is a Tier 4 question rather than a Tier 2 or 3 question? The classification presupposes a meta-classifier that can sort questions into tiers — but that meta-classifier itself is not described.  
   **Recommendation:** For (a), add a brief discussion of borderline cases and the decision rule — perhaps framing it as: "When scholarly disagreement reflects fundamentally different methodological commitments (e.g., textual criticism vs. rhetorical analysis), the question likely belongs at Tier 3." For (b), acknowledge the meta-classification challenge explicitly and note that in the prototype, tier assignment is initially performed by the system prompt + classifier combination described in §3.3, with human correction as the quality backstop. Estimated effort: small–medium.

5. **[§5.2 — Techno-Gnosticism Anti-Patterns]** — The three anti-patterns (resist disembodiment, resist decontextualisation, resist epistemic gnosticism) are clearly stated and persuasively motivated. This section works. But the connection to *agent design* is asserted rather than demonstrated. "Resist disembodiment" is translated as "present contextual metadata alongside textual analysis" — which is a good design decision but is essentially just good metadata practice, not something uniquely motivated by the techno-gnosticism critique. A secular UX designer would make the same recommendation.  
   **Recommendation:** Strengthen the connection by showing what the techno-gnosticism critique adds *beyond* standard good practice. The distinctive contribution might be: standard metadata practice includes date and provenance; a techno-gnosticism-aware system would also present *liturgical context* and *communal reception history* — metadata categories that only make sense if you take seriously the claim that texts are embedded in lived religious practice, not merely in historical dates and library shelves. Estimated effort: small.

6. **[§6.3, ¶3–6 — Personalism → Architecture Translation]** — **This is the paper's most important and most vulnerable section.** The mapping from personalist principles to design decisions is the paper's unique selling point. Let me be honest about where it stands.

   **What works:** The relational ontology → narrative memory mapping is convincing. The idea that if persons are constituted by relationships, then the research process is a relational encounter, and the agent must preserve interpretive continuity — this hangs together. The subsidiarity → graduated autonomy mapping is also strong; subsidiarity is a structural principle and graduated autonomy is a structural implementation.

   **What's weaker:** The inviolable dignity → non-substitution mapping is *true* but *thin*. Any responsible AI designer would argue for human-in-the-loop on interpretive judgments — you don't need Wojtyła to get there. The paper needs to show what personalist anthropology adds that secular human-centered AI doesn't already provide. What does "inviolable dignity" mean architecturally that "user autonomy" (Floridi and Cowls's principle) doesn't? One candidate answer: personalist dignity implies that the interpretive act has *formative* significance for the person — it's not just about getting the right answer but about the scholar's growth through the encounter with the text. The *Laborem Exercens* reference (work forms the worker) gestures at this but doesn't land it.

   **What needs work:** The narrative constitution → memory tracking mapping. The paper says memory should track "the scholar's evolving *story of understanding*." This is evocative but operationally vague. How does a memory system track a "story" as opposed to a "log"? What makes narrative memory different from versioned note-taking? The answer — that narrative memory preserves argumentative structure, interpretive dead ends, moments of revision — is *stated* but not *grounded in personalist philosophy* specifically enough. Why does personalism demand narrative memory rather than, say, any phenomenological philosophy?  
   **Recommendation:** For the dignity mapping, sharpen the distinction from secular HCAI by emphasizing the *formative* dimension: personalist dignity means the interpretive act is not merely a task to be completed but a constitutive moment in the scholar's intellectual and spiritual formation. An agent that "does the reading" doesn't just produce a wrong answer — it *deprives the person of an encounter*. For narrative memory, connect more explicitly to Ricœur's narrative identity (which the paper already uses in §5.1) — the self is constituted by the stories it tells about itself, including the story of its own understanding. A memory system that reduces this to timestamped facts is a reductive anthropology made technical. Estimated effort: medium–substantial. This is the fix most worth making.

7. **[§4.1, ¶1]** — The claim that "the GNORM pipeline's CRF achieves 97.8% accuracy on legal reference annotation in the *Liber Extra*, compared to Latin BERT's 92.4% on the same task" is presented as a direct head-to-head comparison. But this requires a citation for the Latin BERT performance on legal reference annotation specifically. If Latin BERT's 92.4% is on a different task (e.g., POS tagging), the comparison is misleading.  
   **Recommendation:** Verify whether the 92.4% figure is from a direct comparison on the same legal annotation task or from a different benchmark. If the latter, reframe the comparison: "The CRF achieves 97.8% accuracy on legal reference annotation, while Latin BERT's best performance on comparable structured annotation tasks reaches approximately 92%." Estimated effort: small but important for credibility.

8. **[§2.3 — Narrative Memory]** — The section effectively surveys MemGPT, A-MEM, and Zep, but the argument for "narrative memory" as a genuinely novel concept could be strengthened. The paper asserts that "no existing system implements" narrative memory but doesn't fully distinguish it from what existing systems *do* implement. MemGPT's self-managed memory hierarchy already preserves context across sessions; A-MEM's Zettelkasten linking already builds associative networks. What specifically is *narrative* memory, as opposed to *persistent, linked, hierarchical* memory?  
   **Recommendation:** Define narrative memory more precisely by contrast. The distinctive features might be: (a) it preserves *argumentative structure* (not just facts but the logical relationships between claims), (b) it tracks *revision events* (when and why an interpretation changed), and (c) it maintains *productive tensions* (unresolved questions that drive inquiry forward, rather than resolving them). State these criteria explicitly. Estimated effort: small.

### Sections that passed clean on argumentative quality

- §3.3 (Implementation Pathways) — the dual-path epistemological classification is well-argued and technically grounded
- §4.2 (Computational Analysis of Religious Corpora) — the PASSIM/Sefaria/Protestant comparison is empirically well-supported
- §6.1 (AI-in-the-Loop Reframing) — concise and well-cited
- §6.4 (MCP as Relational Infrastructure) — the "brain in a jar" metaphor earns its keep; the theological significance of grounded vs. ungrounded outputs is convincingly drawn


---

## Pass 3: Voice and Style

### Issues Found

1. **[Formal Transitions — Multiple Sections]** — Several "Furthermore" / "Moreover" / "In conclusion"-style transitions survive:
   - §4.2 uses "More recently" three times across the section — not a forbidden transition per se, but repetitive
   - §6.3, ¶1: "These principles are admirable. They are also, as architectural guidance, almost entirely abstract." — This is *good* voice. Keep this.
   - §7.1, ¶2: "RESILIENCE participates in the SSH Open Cluster Governing Board, connecting it to CESSDA, CLARIN, DARIAH..." — reads like an institutional report, not the author's voice
   - §5.1, ¶1: "The most significant theoretical development for situating..." — reused from §2.1. This exact phrasing appears in both places.  
   **Recommendation:** Search-and-replace for "Furthermore," "Moreover," "It is important to note" — I didn't find these specific phrases, which is good. But §7 in particular lapses into reportorial prose that lacks the author's characteristic rhetorical energy. The fix isn't mechanical; it's about re-engaging the voice in the sections that read as survey rather than argument. Estimated effort: small (targeted revisions in §7).

2. **[AI Clichés]** — I checked systematically for the forbidden list. Results:
   - "delve" — not found ✓
   - "navigate" — not found ✓
   - "leverage" — not found ✓
   - "crucial" — appears once, in §3.1: "This is a critical distinction" (uses "critical" not "crucial") — borderline but acceptable
   - "tapestry" — not found ✓
   - "in the ever-evolving landscape" — not found ✓
   - "landscape" — appears 7 times ("research landscape," "technical landscape," "digitisation landscape," "interpretive landscape," etc.). This is borderline. "Landscape" is a legitimate metaphor when used once or twice but becomes an autopilot word at seven occurrences.  
   **Recommendation:** Replace 4–5 of the 7 "landscape" uses with more specific terms: "terrain," "field," "ecosystem," "state of affairs," or simply restructure the sentence to avoid the metaphor. Keep "interpretive landscape" and "digitisation landscape" — those are the most natural. Estimated effort: trivial.

3. **[Repetition — Five-Gap Statement]** — The five gaps are stated, in whole or in part, in: §1 (Introduction), §2.4 (Critical Gap), §3.1 (opening), §4.3 (closing reference to "third convergent gap"), §5.4 (five philosophical gaps listed), §7.3 (five infrastructure gaps), §8.1 (architecture decisions), and §9 (Conclusion). Some repetition is structural and necessary (Introduction and Conclusion should mirror). But the mid-paper restatements (§5.4 especially) feel like the paper is reminding the reader of its argument rather than developing it.  
   **Recommendation:** In §5.4, don't re-list all five gaps. Instead, identify the *philosophical* gaps specific to §5 and note how they map onto the broader five-gap framework: "These five philosophical lacunae correspond to the broader convergent gaps mapped in this synthesis — specifically, Gaps 2 and 4." This signals structure without repetition. Estimated effort: trivial.

4. **[Sentence Variation]** — The author's preferred style calls for dramatic sentence-length variation. The paper mostly achieves this. §1 is exemplary: "The computer helped *find* things. It did not pretend to *understand* them." — short, punchy, effective. §6.3's opening on the Rome Call is also good: "These principles are admirable. They are also, as architectural guidance, almost entirely abstract." But §4.1 and §7.1–7.2 flatten into consistently mid-length sentences (15–25 words) without the punchy short sentences or the long flowing ones that characterize the author's best prose.  
   **Recommendation:** During revision, specifically target §4.1 and §7 for sentence-length variation. One technique: after a technical paragraph with three mid-length sentences, add a single short sentence that crystallizes the point. "The CRF trains in 21 minutes on a desktop CPU. This matters." Estimated effort: small.

5. **[Metaphors]** — Inventory of major metaphors:
   - **Hermeneutical circle as graph** (§2.2): Works well. The mapping is precise enough to be argumentatively productive.
   - **Zettelkasten as theological method** (§2.3): Works. The connection between Luhmann's slip-box and theological associative reasoning is apt.
   - **"Brain in a jar" for isolated LLMs** (§6.4): Works and is memorable. Good coinage.
   - **"Third horizon"** (§1, ¶3): Ambitious. See Pass 2, Issue 1. Needs development or qualification.
   - **"Epidemic of penalised uncertainty"** (§3.1): Slightly overwrought — "epidemic" implies contagion, which doesn't quite fit. Consider "regime of penalised uncertainty" or simply "the systematic penalisation of uncertainty."
   - **"Topology of authority"** (§4.3): Excellent. Precise and evocative for describing the spatial relationship between text, gloss, and super-gloss.  
   **Recommendation:** Trim "epidemic" → "regime" in §3.1. Develop or qualify "third horizon" per Pass 2. All other metaphors are pulling their weight. Estimated effort: trivial.

6. **[Unnecessarily Academic Phrasing]** — A few passages lapse into the generic academic tone the author's style guide explicitly rejects:
   - §5.1, ¶2: "For agent design, the Gadamer/Ricoeur divide has direct architectural consequences" — perfectly fine content, but the construction is standard-issue academic. A more characteristic rendering: "Here's where it gets architectural..."
   - §7.1, ¶1: "The institutional infrastructure for digital religious studies in Europe has matured considerably over the past five years, though unevenly." — competent but anonymous. The author's voice is absent.  
   **Recommendation:** During the voice-polishing pass, target the openings of §5.1, §7.1, and §7.2 specifically. These sections' *content* is strong; the *voice* needs the author's characteristic warmth, wit, and rhetorical buildup. Estimated effort: small.

### Sections with strong voice throughout

- §1 (Introduction) — the opening three paragraphs are excellent: vivid, rhythmically varied, philosophically precise
- §3.1 (Why Epistemic Modesty Requires Its Own Architecture) — the Gadamer paragraph has real force
- §6.3 (Christian Personalism as Design Ethic) — the "These principles are admirable. They are also..." passage is pitch-perfect
- §9 final paragraph — "an agent that is, in the end, not intelligent but *instrumental*" lands well


---

## Pass 4: Technical Accuracy and Citations

### Issues Found

1. **[Bibliography Gap — Cited but not in bibliography]** — The following sources are cited in the text but do not appear in the References section:
   - **"Somanunnithan (2025)"** — cited in §2.2 for the CrewAI three-agent demonstration. Listed in "Sources Requiring DOI Verification" as grey literature but *not* in the main bibliography. Either add it to the bibliography with appropriate caveats or remove the in-text citation and describe the demonstration without attribution.
   - **"BiblIndex" project** — referenced in §4.2 but has no bibliographic entry. Add a reference (the project has published documentation).
   - **"BLAST" bioinformatics method for patristic text reuse** — referenced in §4.2 but has no citation. Needs attribution.
   - **LatinPipe / EvaLatin 2024** — referenced in §4.1 but has no bibliographic entry. The EvaLatin 2024 shared task proceedings should be cited.
   - **DISSINET project** — referenced in §4.1 but has no bibliographic entry. Cite their publications (Zbíral et al.).
   - **Sefaria MCP server (2025)** — referenced in §4.2 and §6.4 but has no formal citation. This is a software release; cite the GitHub repository or announcement.
   - **Newman, "illative sense"** — referenced in §2.3 but *An Essay in Aid of a Grammar of Assent* (1870) is not in the bibliography.
   - **Valleriani, Max Planck** — referenced in §4.2 and §7.3 but has no bibliographic entry.
   - **Pope Leo XIV** — quoted in §6.3 but no specific document is cited (World Media Day message? Specific encyclical?). Add source.

   **Recommendation:** Add proper bibliographic entries for each of the above. For grey literature (Sefaria MCP, BLAST application, BiblIndex), provide URLs with access dates. Estimated effort: medium (requires bibliographic lookup).

2. **[Bibliography Gap — In bibliography but not cited in text]** — The following entries appear in the bibliography but I could not find corresponding in-text citations:
   - **Le Duc, A. (n.d.). "Towards a Cybertheology..."** — the SSRN preprint. Le Duc's 2026 keynote *is* cited, but this earlier work appears uncited. Either cite it in §5.3 (where cybertheology is discussed) or remove.
   - **Wu, Q. et al. (2023). "AutoGen..."** — Referenced in the framework comparison? Yes, §2.2 discusses AutoGen but doesn't use an in-text citation with "(Wu et al., 2023)." The bibliography entry exists but the in-text reference is by product name only. Add a parenthetical citation. Trivial fix.

3. **[Pipeline Technical Reference Cross-Check]** — Checking claims against `pipeline_technical_reference.md`:

   (a) **§3.3 — `mark_source` prefixes.** The paper lists: `RULE|`, `ABBREVIATION|`, `MATCH|`, `PREPOST|`, `CRF|`. The pipeline reference lists the same five plus `SOURCE|` (expert annotation / training data). The paper omits `SOURCE|`. This isn't technically wrong (the paper is describing pipeline-generated annotations, not training data labels), but for completeness the omission should be noted.

   (b) **§4.3 — "41,784 legal references across approximately 1,795 distinct canonical source nodes."** The pipeline reference says "~1,795 unique legal source nodes and ~41,784 reference edges." These are consistent. ✓

   (c) **§4.3 — "97.8% accuracy."** Pipeline reference confirms: "97.8% accuracy (CRF rich config)." ✓

   (d) **§4.1 — "CRF trains in 21 minutes on a desktop CPU and produces a 1.1 MB model."** Pipeline reference confirms both figures. ✓

   (e) **§3.3 — The paper says the `Tipo` field preserves provenance in the INCEpTION roundtrip.** Pipeline reference confirms: "Preserved in INCEpTION roundtrip via `Tipo` field." ✓

   (f) **§8.2 — "Code inspection of the CIC_annotation repository confirmed the six-layer hybrid architecture."** Pipeline reference confirms six layers with the same descriptions. ✓

   (g) **§8.2 — "the CRF engine is label-agnostic, meaning domain adaptation concentrates at the pipeline edges."** Pipeline reference confirms: "The ML core will learn whatever labels the training data contains." ✓

   (h) **§4.3 — The paper describes "six-layer hybrid architecture combining rule-based regex patterns, abbreviation dictionaries, trie matching with statistical gap prediction, CRF machine learning, and structural parsing."** This is five items, not six. The pipeline reference shows six layers: (1) rules/trie+regex, (2) abbreviation dictionary, (3) trie exact + statistical gap prediction (PREPOST), (4) CRF, (5) structural regex (chapter/title/lemma), (6) merge + post-processing. The paper collapses layers 1 and 3 (both involve trie matching) and omits the merge layer. This is a minor inaccuracy but might confuse readers who inspect the codebase.  
   **Recommendation:** Either say "six processing stages" and enumerate them correctly, or say "multi-layer hybrid architecture" without committing to a count. Estimated effort: trivial.

   (i) **§4.1 — "Latin BERT's 92.4% on the same task."** This figure does not appear in the pipeline technical reference. It needs an independent citation source. See Pass 2, Issue 7.

4. **[Source A Cross-Check]** — Checking claims against the literature synthesis:

   (a) **Source A says "three-tier epistemic classification"** with a parenthetical that actually lists four tiers (including "matters of faith and doctrine"). The paper correctly uses "four-tier." This is a self-correction from Source A's numbering inconsistency. ✓

   (b) **Source A says Kommers et al. has "37 co-authors."** The paper says "thirty-four additional co-authors" plus three named. 34 + 3 = 37. Consistent. ✓

   (c) **Source A says Manuscriptorium has "400,000+ descriptive records" and "110,000+ digitised documents from 139 partners in 24 countries."** The paper says "360,000+ descriptive records, 33 million digitised pages, and 130,000+ digitised documents from more than 180 institutions in approximately twenty countries." These figures are *different* — Source A gives 400K/110K/139/24; the paper gives 360K/130K/180/20. Both likely derive from different access dates to the Manuscriptorium website, which updates its statistics. But the discrepancy should be resolved by checking the current figures.  
   **Recommendation:** Verify Manuscriptorium statistics at manuscriptorium.com and use current figures with an access date. Estimated effort: trivial.

   (d) **Sefaria user count:** Both Source A and the paper say "775,000 monthly users." Consistent. ✓

5. **[Sources Requiring Verification]** — The paper transparently lists six sources requiring DOI verification at the end of the bibliography. This is good scholarly practice. However, two of these sources are cited in the *main text* without qualification:

   - **Adeboye et al. (2025)** — cited in §5.3 without a "venue unconfirmed" hedge. The text says simply "Adeboye et al. (2025) document that encoding oral divination verses..."
   - **"AI as Interpretive Aid in Qur'anic Stylistics" (2025)** — referenced in §5.3 for the *i'jaz* doctrine discussion. The bibliography notes say "Author(s), venue, and DOI unconfirmed. Not included in the bibliography pending verification." But the claim still appears in the main text without qualification.  
   **Recommendation:** Either verify these sources before publication or add a qualifying phrase in the text: "Adeboye et al. (2025; venue pending confirmation)." For the Qur'anic stylistics reference, either find the actual publication or attribute the *i'jaz* discussion to a verified source on computational Qur'anic analysis. Estimated effort: small–medium (requires literature search).

6. **[§2.1 — Piotrowski (2026) DOI]** — The DOI given is `10.1007/978-3-032-08697-6_2`. The Springer LNCS prefix is typically `978-3-031-...` or `978-3-030-...`. The `032` is unusual and may be a typo for `031` or a valid new range. Verify.  
   **Recommendation:** Confirm DOI resolves correctly. Estimated effort: trivial.

7. **[§6.3 — Vatican document names]** — The paper references *Humanae Dignitatis* (2023) as a Vatican follow-up to the Rome Call. I could not verify a Vatican document by this exact title. The 2024 Vatican declaration on human dignity is *Dignitas Infinita*. If this is a different, earlier document, it needs a more precise citation. If it's a confusion with *Dignitas Infinita*, the date is wrong (2024, not 2023).  
   **Recommendation:** Verify the exact title and date of this document. If it doesn't exist under this name, correct or remove. Estimated effort: small but important for credibility.

### Sections that passed clean on technical accuracy

- §2.2 (Framework Comparison) — technical claims about LangGraph, CrewAI, AutoGen are accurate
- §3.3 (Implementation Pathways) — pipeline integration described accurately against reference
- §4.3 (GNORM) — all verifiable claims match the pipeline reference
- §4.4 (OCR/HTR) — technical details consistent with Source A
- §6.4 (MCP) — accurate description of protocol and adoption timeline


---

## Priority Fix List

Ranked by impact on paper quality. Each fix is keyed to a specific pass and issue number.

| Rank | Fix | Pass | Issue | Section | Effort | Why It Matters |
|:---:|-----|:---:|:---:|---------|:---:|----------------|
| 1 | **Sharpen the personalism → architecture bridge**, especially the dignity and narrative mappings | P2 | 6 | §6.3 | Substantial | This is the paper's unique claim. If it isn't convincing, the paper becomes a good survey rather than a contribution. |
| 2 | **Add convergence paragraph to §9** showing how the five gaps synergize, not just coexist | P1 | 5 | §9 | Medium | Fulfills the Introduction's central promise. Currently the weakest structural moment. |
| 3 | **Specify Tier 2/3 boundary and Tier 4 recognition mechanism** for the epistemic classification | P2 | 4 | §3.2 | Small–Medium | The four-tier framework is the paper's standalone methodological contribution. Borderline cases and the meta-classifier need addressing for reviewers to take it seriously. |
| 4 | **Fix missing bibliography entries** (Newman, BiblIndex, BLAST, LatinPipe, DISSINET, Valleriani, Sefaria MCP, Pope Leo XIV source) | P4 | 1 | Bibliography | Medium | 10+ citation gaps is a lot for a paper of this ambition. Reviewers will catch these. |
| 5 | **Verify *Humanae Dignitatis* (2023)** and Latin BERT 92.4% comparison figure | P4 | 6, 7 | §6.3, §4.1 | Small | If either is wrong, it damages credibility on factual precision — ironic for a paper about epistemic modesty. |
| 6 | **Trim §2.2** from ~2,800 to ~2,000 words | P1 | 2 | §2.2 | Medium | The section is strong but bloated. The comparison table should do more work; the prose should do less. |
| 7 | **Resolve §8 tense issues** (convert plans to results after Feb 27) | P1 | 4 | §8.2 | Small | Currently reads as half-plan, half-report. Needs a clean pass post-fellowship. |
| 8 | **Replace 4–5 of 7 "landscape" uses** | P3 | 2 | Multiple | Trivial | Easy win that removes the only stylistic autopilot pattern in the paper. |
| 9 | **Develop or qualify the "third horizon" concept** | P2 | 1 | §1, ¶3 | Small–Medium | It's either the paper's most memorable concept or its most exposed philosophical weakness. Can't remain in the middle. |
| 10 | **Resolve unverified sources** (Adeboye, Qur'anic stylistics) — either verify or hedge in-text | P4 | 5 | §5.3, Bib. | Small–Medium | Two claims in the main text rest on unverified sources. Reviewers may check. |

---

## Overall Assessment

This is a strong paper — substantially above what most interdisciplinary syntheses achieve. The five-gap framework is well-conceived and threads consistently through the argument. The technical sections (§3.3, §4.3) are grounded in actual code inspection, not hand-waving. The voice, where it appears, is distinctive and engaging.

The paper's greatest strength is the *range* of its synthesis — 80+ sources across five domains, held together by a coherent argument. Few scholars could write §2 (agent architectures) and §5 (hermeneutical philosophy) and §7 (CEE infrastructure) with equal competence. The GNORM pipeline integration (§3.3, §4.3) grounds the otherwise theoretical argument in concrete technical reality.

The paper's greatest vulnerability is the personalism → architecture bridge (§6.3). It is the paper's most distinctive claim and the one most likely to draw reviewer scrutiny. Right now it is *stated* more than it is *argued*. Strengthening this section — particularly by showing what personalism adds that secular HCAI doesn't already provide, and by grounding narrative memory in Ricœurian narrative identity rather than generic memory architecture — would transform the paper from very good to excellent.

The bibliography needs housekeeping. Ten missing entries and two unverified sources create unnecessary risk. These are all fixable with modest effort.

If the top five items on the Priority Fix List are addressed, this paper is ready for submission to *AI & Society*.

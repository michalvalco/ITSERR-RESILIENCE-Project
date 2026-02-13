# INTEGRATED RESEARCH SYNTHESIS: Detailed Section-by-Section Outline

**Working title:** *Designing Ethically-Grounded AI Agents for Religious Studies Research: A Comprehensive Research Synthesis*  
**Purpose:** Paragraph-level integration map for building the final report from Source A (Claude Report) and Source B (GEM Report)  
**Created:** February 11, 2026  
**Companion to:** `integrated_report_strategy.md` (in PKB)

---

## NOTATION KEY

- **[A]** = Source A (Claude Report, ~142 sources, .md in PKB)
- **[B]** = Source B (GEM Report, ~33 sources, .docx in PKB)
- **[NEW]** = New material to write (not in either source)
- **[MERGE]** = Content in both sources; synthesize best of each
- **[SEARCH]** = Requires targeted literature search before writing
- **⚠️ TENSION** = Sources disagree or frame differently; reconciliation needed
- **🔑 KEY MOVE** = Critical argumentative step for the section's coherence

---

## SECTION 1: Introduction — The Theological Turn in Artificial Intelligence
**Estimated length:** 800–1,000 words  
**Source priority:** [B] framing + [A] scholarly precision  
**Function:** Set the scene; establish five-domain structure; frame the contribution gap

### ¶1.1 — Opening: The shift from digitization to agentification
- [B] "For decades, the Digital Humanities operated primarily as a discipline of digitization and retrieval... the advent of 'Agentic AI'—systems capable of autonomous reasoning, tool use, and multi-step workflow orchestration—has fundamentally altered the research landscape."
- [B] The "from search to synthesis" framing — clean and quotable, keep it
- [NEW] Update with 2026 context: note that agentic AI has moved from theoretical to production-ready (LangGraph, CrewAI mainstream; MCP adopted by all major providers)
- 🔑 KEY MOVE: Establish that the transition is not merely technical but *epistemological* — it changes what counts as "knowing" a text

### ¶1.2 — The hermeneutical problem: the "third horizon"
- [B] "When an AI agent mediates this encounter, it introduces a 'third horizon'—one constituted not by tradition or lived experience, but by statistical probability and training weights."
- [A] Connect to Gadamer's *Horizontverschmelzung* (more precise than [B]'s gloss)
- [NEW] Brief signal that this is not merely a philosophical concern but shapes concrete architecture decisions (previewing Section 6)
- Tone: Set the stakes — this is not about whether AI *can* help, but about what kind of help preserves vs. flattens hermeneutical complexity

### ¶1.3 — The five-domain structure of the synthesis
- [A] The five domains (agent architectures, computational philology, philosophy of AI, human-centred design, European infrastructure)
- [NEW] Brief paragraph announcing the structure, but not as a mechanical table of contents — more as an intellectual map of the territory
- [NEW] One sentence positioning the fellowship context: "This synthesis was developed during an ITSERR Transnational Access Fellowship at the University of Palermo (February 2026), in direct collaboration with the GNORM project team."

### ¶1.4 — The contribution claim
- [A] The five-gap convergence analysis (from Claude's conclusion) — preview here, develop in full in Section 9
- 🔑 KEY MOVE: State the claim compactly: no agentic system for theological research exists; personalist anthropology has never been translated into AI architecture; Protestant corpora are computationally underserved; epistemic modesty for interpretive domains is untheorised; ITSERR's tools await agentic orchestration
- Tone: Confident but not grandiose. "The infrastructure exists. What is missing is the bridge."

---

## SECTION 2: AI Agent Architectures for Interpretive Humanities Work
**Estimated length:** 3,000–3,500 words  
**Source priority:** [A] for scholarly depth; [B] for metaphors and Table 1  
**Function:** Establish the technical landscape; justify LangGraph; introduce memory and the "no precedent" gap

### §2.1 — Computational Hermeneutics as an Emerging Paradigm

#### ¶2.1.1 — The Turing Institute synthesis
- [A] Kommers, Ahnert, Antoniak, et al. (2025) — 37 co-authors, three interpretive challenges: situatedness, plurality, ambiguity
- [A] Three evaluation principles (iterative, people-inclusive, culturally contextual) → translate these into agent design requirements
- 🔑 KEY MOVE: Establish that this is not a niche concern — the leading DH research institution has identified interpretive evaluation as the central challenge

#### ¶2.1.2 — Genealogy of computational hermeneutics
- [A] Mohr, Wagner-Pacifici & Breiger (2015) — foundational definition
- [A] Piotrowski (2026) — interpretation as model construction, computational hermeneutics demands structured representations
- [A] Henrickson & Meroño-Peñuela (2023) — "hermeneuticity" as measurable quality; prompt engineering can increase it
- Tone: Build the intellectual lineage quickly — this is scaffolding for the argument, not the argument itself

#### ¶2.1.3 — The theological bias problem
- [A] Elrod (2024) — five LLMs queried with Hebrew Bible texts; LLMs privilege progressive and Christian frames; hermeneutical nuance lost
- [A] EPJ Data Science (2025) — hybrid human-LLM workflow preserving "hermeneutic value"
- 🔑 KEY MOVE: These aren't abstract risks; they're measured empirical findings. An agent for theological research must be designed with awareness of specific directional biases.

### §2.2 — Comparative Analysis of Agent Frameworks

#### ¶2.2.1 — LangGraph: graph-based control for theological research
- [MERGE] Both sources cover this; [A] is more precise on technical capabilities, [B] provides "State as Locus" metaphor
- [A] Graph-based architecture models the hermeneutical circle naturally (parts ↔ whole)
- [A] Built-in statefulness, HITL checkpoints, short-term and long-term memory, tool integration
- [B] "The State is not merely a collection of variables; it is the *locus* of the hermeneutical act" — KEEP this metaphor
- [B] Auditability: "In religious studies, a hallucinated citation is not just a bug; it is a falsification of tradition" — KEEP
- [A] Reference the Open Deep Research agent (github.com/langchain-ai/open_deep_research)
- [A] Note: CUNY Graduate Center launched first DH agentic AI course (Spring 2025)

#### ¶2.2.2 — CrewAI: role-based collaborative intelligence
- [MERGE] [A] scholarly detail + [B] theological application
- [B] "Philologist Agent," "Systematic Theologian Agent" role metaphors — accessible and useful
- [B] Warning about anthropomorphism and "groupthink" reinforcing hallucinations
- [A] Adds: "suitable for modelling scholarly debate" — the DH angle

#### ¶2.2.3 — AutoGen: conversational emergence and digital dialectics
- [MERGE] [A] technical + [B] Scholastic Method metaphor
- [B] "Digital Dialectics" — program "Thomist Agent" and "Scotist Agent" to debate → KEEP as illustration
- [B] Context drift warning — interesting but irrelevant theological speculation
- [A] UserProxyAgent representing human scholar

#### ¶2.2.4 — Comparative table and framework selection
- [B] Table 1 (Comparative Analysis of AI Agent Frameworks) — preserve and expand
- ⚠️ TENSION: [B]'s table is cleaner but less nuanced; [A] adds dimensions (memory type, tool integration). Merge into enhanced table.
- 🔑 KEY MOVE: Justify LangGraph selection explicitly — its graph structure, HITL, and state management make it the natural choice for theological research requiring auditability and interpretive control
- [NEW] Add row for "Theological Suitability" to the table

### §2.3 — Narrative Memory: Beyond Factual Recall

#### ¶2.3.1 — The problem of catastrophic forgetting in long-term research
- [B] "Early AI implementations suffered from 'catastrophic forgetting'... For a religious studies researcher, who may spend years on a single project, this is unacceptable"
- [MERGE] Both sources frame the problem; [B] more accessibly

#### ¶2.3.2 — MemGPT/Letta: the OS-inspired hierarchy
- [A] Packer et al. (2023) — core memory (RAM analogue), archival memory (disk), recall memory (conversation history)
- [A] Theological mapping: core memory = scholar's evolving interpretive framework; archival memory = consulted corpus and prior analyses
- Full citation with arXiv reference

#### ¶2.3.3 — A-MEM: the Agentic Zettelkasten
- [A] Xu et al. (2025) — Zettelkasten-inspired system with interconnected "notes," keywords, tags, embeddings
- [B] "Agentic Zettelkasten" label — the metaphor is [B]'s but maps to [A]'s technical content
- [B] "Atomic Memories" — single, verifiable, grounded, scoped claims
- [A] "superior to MemGPT for open-ended tasks and directly relevant to modelling how a theological agent builds webs of interpretive connections"
- 🔑 KEY MOVE: The Zettelkasten is not just a storage pattern; it mirrors how theological scholarship actually works — building networks of interconnected insights over years

#### ¶2.3.4 — Zep: temporal knowledge graphs
- [A] Rasmussen et al. (2025) — temporal knowledge graphs tracking how interpretations evolve historically
- [NEW] Brief note on relevance for tracking *reception history* (Wirkungsgeschichte) of theological concepts

#### ¶2.3.5 — The narrative memory gap
- [A] "No work explores 'narrative memory' specifically—the capacity to maintain a coherent interpretive narrative across sessions, tracking not just facts but evolving understanding, interpretive commitments, and unresolved tensions."
- 🔑 KEY MOVE: This is the first of the five gaps. State it precisely. This is architecturally novel.
- [B] "Rolling Summaries" as practical implementation pattern — structured narrative updated after every interaction

### §2.4 — The Critical Gap Statement
- [A] "No published work applies multi-agent orchestration frameworks to theological or religious studies research."
- [A] Key research groups table: Turing Institute, UC Berkeley, Oxford OATML, UW/Allen AI, CUNY
- [A] Priority readings list (5 sources) — preserve for operational utility

---

## SECTION 3: Epistemic Modesty and Calibrated Confidence
**Estimated length:** 1,500–2,000 words  
**Source priority:** [A] for technical framework; [B] for philosophical motivation  
**Function:** Elevate epistemic modesty from a subsection to the standalone treatment it deserves  
**Rationale for standalone section:** Both reports identify this as central to the project's distinctive contribution but neither gives it structural prominence. This section signals its importance.

### §3.1 — Why Epistemic Modesty Requires Its Own Architecture

#### ¶3.1.1 — The philosophical motivation: the "Shadow" of the agent
- [B] Jungian framing — "the AI's 'hallucinations' and biases as its Shadow"
- [B] "An ethically grounded agent must be designed to 'confront its shadow.' It should not mask uncertainty with confident prose."
- [NEW] Connect to Valčo's personalist framework: if the person is constituted by narrative and relational encounter, then an AI that feigns certainty distorts the relational encounter with the text
- Tone: This is where philosophy meets engineering. Don't let it feel merely decorative.

#### ¶3.1.2 — The technical landscape: uncertainty estimation in LLMs
- [A] Wen et al. (2025), TACL — definitive survey on LLM abstention
- [A] Kuhn, Gal & Farquhar (2023) — semantic entropy for uncertainty estimation (ICLR 2023)
- [A] Farquhar et al. (2024) — hallucination detection using semantic entropy (Nature)
- [B] "Predict-Calibrate Principles" and the "prediction gap" concept
- ⚠️ TENSION: [B] uses "Free Energy Principle" framing which is speculative in this context. Use [A]'s more grounded semantic entropy approach; mention [B]'s calibration language as complementary.

### §3.2 — The Three-Tier (Four-Tier) Epistemic Classification

#### ¶3.2.1 — The categorical gap in existing calibration work
- [A] "All existing calibration work targets factual Q&A. For theological research, the agent needs a three-tier epistemic classification"
- 🔑 KEY MOVE: This is the second major gap. Existing confidence calibration addresses *factual correctness*; theological research requires calibration across a *spectrum of epistemic modalities*.

#### ¶3.2.2 — The framework itself
- [A] Four tiers (Claude report actually specifies four, not three):
  1. **FACTUAL/HISTORICAL** — "Paul wrote Romans around 57 CE" — verifiable, datable
  2. **SCHOLARLY CONSENSUS** — "Most scholars date Mark as the earliest Gospel" — acknowledged disagreement exists
  3. **INTERPRETIVE/CONFESSIONAL** — "This passage has been read as..." — multiple valid traditions
  4. **MATTERS OF FAITH AND DOCTRINE** — full deferral to human judgment
- [NEW] Map each tier to specific agent behaviours:
  - Tier 1: Agent presents with citation; high confidence
  - Tier 2: Agent presents with "according to..." framing; flags disagreement
  - Tier 3: Agent presents multiple readings; never selects one
  - Tier 4: Agent refuses to generate; offers to retrieve relevant authorities for the scholar's own judgment
- [NEW] Connect to prototype implementation: these map to the FACTUAL / INTERPRETIVE / DEFERRED tags in the existing codebase (reference `epistemic/indicators.py`)

### §3.3 — Implementation Pathways

#### ¶3.3.1 — Belt-and-suspenders: prompt + classifier
- [NEW] Reference the existing prototype's approach: system prompt instructs the LLM to add epistemic tags inline; classifier validates and adds missing tags
- Connect to itserr_reference_mapping.md: the pipeline is `classify_sentence()` → citation check → theological term detection → marker scoring → fallback
- Note the known limitation: sentence splitting via regex (TODO: NLTK/spaCy)

#### ¶3.3.2 — GNORM confidence integration
- [A] GNORM confidence mapping: ≥0.85 → FACTUAL; <0.85 → INTERPRETIVE; <0.50 → INTERPRETIVE with review flag
- [NEW] This is one of the concrete integration points with Arianna's team — confirm these thresholds during the technical briefing

#### ¶3.3.3 — The LLM verification step (not yet implemented)
- [A] Design specifies LLM verification for ambiguous cases; not yet coded
- [NEW] Flag this as a Week 2 priority during the fellowship
- Note: this is where semantic entropy methods (Kuhn et al.) would be integrated

---

## SECTION 4: Computational Approaches to Religious and Legal Texts
**Estimated length:** 2,500–3,000 words  
**Source priority:** [A] substantially stronger; [B] for accessibility and GNORM description  
**Function:** Survey the computational landscape for religious texts; identify Protestant gap  
**Searches needed:** Search 2 (Protestant Reformation-era corpus computational analysis)

### §4.1 — Latin NLP: From Classical to Medieval

#### ¶4.1.1 — The transformer revolution in Latin
- [A] Latin BERT (Bamman & Burns, 2020) — 642.7M words, state-of-art POS tagging
- [A] LaBERTa and PhilBERTa (Riemenschneider & Frank, 2023, ACL) — monolingual Latin + classical trilingual
- [A] LatinPipe (EvaLatin 2024 winner, ÚFAL Prague) — fine-tuned concatenation approach

#### ¶4.1.2 — The medieval Latin problem
- [A] eFontes project (arXiv:2407.00418) — accuracy drops: POS tagging 83.29%, lemmatisation 92.60% on medieval texts
- 🔑 KEY MOVE: "Domain adaptation from classical to medieval Latin remains an unsolved problem" — this is directly relevant to the Stöckel corpus
- [A] DISSINET project (Masaryk University, Brno) — CASTEMO for knowledge graphs from medieval inquisition records

#### ¶4.1.3 — When simpler models win: the CRF case
- [MERGE] Both sources cover CRF vs. transformers; use [A]'s precision, [B]'s narrative
- ⚠️ TENSION: [B] says "CRFs outperformed Latin BERT by over 5%" — this is domain-specific (legal reference annotation), not general. [A] is precise: CRF achieved 97.8% vs. Latin BERT's 92.4% on this specific task.
- 🔑 KEY MOVE: Frame as "right tool for the right task" — CRFs excel at structured, formulaic annotation; transformers at contextual understanding. This pragmatism is itself a design principle.
- [B] Sustainability argument: CRF on desktop CPU; BERT requires GPU. For sustainable infrastructure, lighter models are preferable.

### §4.2 — Computational Analysis of Religious Corpora

#### ¶4.2.1 — Patristic scholarship leads: the PASSIM Project
- [A] ERC-funded, Radboud University Nijmegen (Shari Boodts) — 5,000+ late-antique Latin sermons, 12,000+ medieval manuscripts
- [A] Network visualisation of textual relationships; authorship verification (Siamese networks, AUC-ROC 0.855)
- [A] Macchioro (2021), Boodts & Denis (2023) references

#### ¶4.2.2 — Talmudic computational scholarship
- [A] Waxman (2021) — graph database: 630 rabbis, 1,217 unique interactions in the Babylonian Talmud
- [A] Sefaria MCP server (2025) — Claude/ChatGPT querying authoritative Jewish texts in real-time → directly relevant model
- [NEW] Note connection to GNORM's Talmud expansion (Marco Papasidero's work at Palermo)

#### ¶4.2.3 — The Protestant gap
- [A] "Protestant theological corpus computational analysis is significantly underrepresented."
- [A] No major NLP project on Luther's complete works, Melanchthon's *Loci Communes*, or the Book of Concord
- [A] Reformation studied computationally almost exclusively through social/historical lenses (correspondence networks, print culture)
- [SEARCH] Search 2 results — incorporate any findings on Reformation-era computational work
- 🔑 KEY MOVE: This is the third major gap. Directly aligned with Valčo's expertise. The Leonard Stöckel corpus project addresses it.

### §4.3 — GNORM and 3D Visualization

#### ¶4.3.1 — What GNORM does
- [MERGE] Both sources cover this; [B] gives the phenomenological description, [A] gives the technical detail
- [B] "Religious and legal texts are rarely linear. They are stratified" — KEEP
- [B] The "topology of authority" framing — central text surrounded by glosses surrounded by super-glosses
- [A] Technical facts: 41,784 references, CRF 97.8%, 21 min training, 1.1 MB model, 1,795 distinct sections
- [A] Code availability: github.com/aesuli/CIC_annotation

#### ¶4.3.2 — GNORM's significance for the project
- [A] Pragmatic methodological selection as design principle
- [A] *Allegationes* as performative acts, not mere references — parallels concern about hermeneutical complexity
- [A] Low-resource reproducibility — small team, desktop hardware, open-source code
- [NEW] Connection to fellowship: the GNORM integration placeholder in the prototype (`integrations/gnorm.py`) awaits confirmation of real API details from Arianna's team

#### ¶4.3.3 — UbiQuity and intertextuality
- [B] WP8 — Bible/Qur'ān commentaries as "places of memory"
- [B] Node-based interface making "thinking process" visible — contrast with generative AI's opacity
- [A] "Similar citation network challenges as your Stöckel corpus"

### §4.4 — OCR and Handwritten Text Recognition

#### ¶4.4.1 — Transkribus and eScriptorium
- [MERGE] [A] more scholarly; [B] gives the "last mile" framing
- [A] Muehlberger et al. (2019); Stokes et al. (2021) for eScriptorium/Kraken
- [A] CREMMA Medii Aevi dataset — 1M+ characters of medieval manuscript ground truth
- [A] Koch et al. (2023) — Bavarian Academy medieval Latin HTR: CER 0.015
- [B] HTR as "rough draft generator" — "the role of the human philologist remains essential for the last 5%"

#### ¶4.4.2 — Implications for the Stöckel corpus
- [NEW] Brief paragraph connecting HTR landscape to the concrete needs of the Leonard Stöckel digitization project
- Note: Stöckel's texts are 16th-century printed, not handwritten — different technical challenges (OCR, not HTR, but layout analysis still matters for marginal glosses)

### §4.5 — Research Groups and Priority Readings
- [A] Research groups table (CIRCSE, ALMAnaCH, ÚFAL, DISSINET, PASSIM, eScripta, Waxman Lab) — preserve
- [A] Priority readings list (5 sources) — preserve

---

## SECTION 5: Philosophy of AI and Hermeneutics
**Estimated length:** 2,500–3,000 words  
**Source priority:** Both strong from different angles — true merge  
**Function:** Establish philosophical foundations; define the contribution space through five under-theorised gaps

### §5.1 — Digital Hermeneutics: A Genealogy

#### ¶5.1.1 — The Capurro–Romele lineage
- [A] Capurro (2010) — defined digital hermeneutics; "digital ontology" vs. "digital metaphysics"
- [A] Romele, Severo & Furia (2020) — definitive synthesis; Dreyfus/Winograd/Flores tradition vs. Mohr/Wagner-Pacifici/Breiger tradition; the Gadamer/Ricoeur divide mapped

#### ¶5.1.2 — Gadamer after ChatGPT
- [MERGE] [A] scholarly detail + [B] accessible framing
- [A] Hornby (2024) — generative AI cannot function as proxy dialogue partner; lacks moral awareness, emotions, epistemological depth; but may serve as "digital form of Gadamerian text"
- [B] "Does an AI have a 'horizon'? It has a 'training distribution.' It does not have *tradition* in Gadamer's sense"
- [B] Design implication: "The AI must be designed as a mediator, not an interpreter. It brings the 'horizon' of the data (patterns, frequencies) to the scholar, who then performs the fusion."
- 🔑 KEY MOVE: The agent should present "pattern," not "meaning"

#### ¶5.1.3 — Ricoeur: suspicion and faith in digital form
- [B] Hermeneutics of suspicion vs. hermeneutics of faith — computational tools naturally align with suspicion (statistical anomalies, authorship attribution)
- [B] The challenge: designing AI that supports the hermeneutics of faith — "slow, meditative interfaces" (GNORM's 3D vis) rather than rapid-fire chatbot summarisation
- [A] Piotrowski (2026) — interpretation as model construction; computational hermeneutics demands structured representations

#### ¶5.1.4 — The Verstehen gap
- [A] Picca et al. (2024) — AI lacks Verstehen due to absence of self-awareness and subjective experience (Diltheyan perspective)
- [B] "There is a fundamental gap between *Verstehen* (interpretive understanding) and Data Processing. The AI agent operates in the realm of Processing."
- [B] ELIZA effect warning — the danger of projecting understanding onto the machine

### §5.2 — Techno-Gnosticism: A Theological Diagnostic for AI Design

#### ¶5.2.1 — The genealogy of techno-gnosticism
- [A] Erik Davis (1998/2015) — TechGnosis; mystical/religious narratives in technological culture
- [A] David Pence (2017, *Religions*) — transhumanism replicates Gnostic vision; Merleau-Ponty's embodiment philosophy; consciousness from body-environment interactions
- [A] 2025 *Religions* article — "divine ethics" as evaluative grammar; "idolatrous re-enchantment" vs. "relational re-enchantment"

#### ¶5.2.2 — Donati's Relational Realism
- [B] Donati — Techno-Gnosticism within the Digital Technological Matrix (DTM)
- [B] DTM as "Generator of Diversity" — decoupling communication from moral matrices; creating "hybrids"
- [B] Antidote: "Relational Realism" — the "person" is an ontological category distinct from the "processor"
- [A] Coeckelbergh (2025) — "Digital Trinity" (datafication, algorithmisation, platformisation) as transhumanism-shaped techno-religion

#### ¶5.2.3 — From diagnosis to design anti-patterns
- [A] Three concrete principles derived from techno-gnosticism critique:
  1. Resist disembodiment (texts are not pure data; they have liturgical, communal, material contexts)
  2. Resist decontextualisation (don't extract propositions from hermeneutical traditions)
  3. Resist "epistemic gnosticism" (more data ≠ better understanding)
- [NEW] Connect these explicitly to agent architecture decisions (previewing Section 6)

### §5.3 — Digital Theology as a Distinct Space

#### ¶5.3.1 — CODEC and the Phillips taxonomy
- [A] Peter Phillips (CODEC, Durham) — field-defining taxonomy; four types of digital theological work
- [A] Phillips, Schiefelbein-Guerrero & Kurlberg (2019, *Open Theology*) — separating digital theology from DH and digital religion
- [B] "Pixelated Text" — the Bible read on screen, fragmented by search algorithms; authority shifts; "crisis of authority"

#### ¶5.3.2 — Current voices: Le Duc, Campbell, the Rome perspective
- [A] Anthony Le Duc (2026) — "technology is never neutral"; "algorithmic mediation"; cybertheology
- [A] Heidi Campbell (2025) — religious AI tools as "charismatic technologies"
- [A] Pope Leo XIV World Media Day 2026 message context

### §5.4 — Prof. Valčo's Published Contributions and Positioning

#### ¶5.4.1 — The personalist framework
- [A] Valčo (2024) — AI algorithms' impact on human values (echo chambers, mimetic desire)
- [A] "Beyond Algorethics" preprint (arXiv:2507.16430) — Pope Francis, Benanti's "algorethics"
- [A] Valčo & Bírová (2024, *Philosophia*) — Kierkegaard's agape personalism, Bonhoeffer, Scheler, Wojtyła

#### ¶5.4.2 — The five under-theorised connections (the contribution space)
- [A] This is the core gap analysis — all five gaps stated precisely:
  1. No systematic framework integrating Gadamerian/Ricoeurian hermeneutics with AI agent architecture
  2. Absence of personalist philosophy in AI agent design
  3. Scarce empirical research on hermeneutical loss when AI processes sacred texts
  4. Techno-gnosticism critique not translated into design anti-patterns
  5. Limited comparative religious perspectives in computational hermeneutics
- 🔑 KEY MOVE: These five gaps define the unique contribution space that no one else currently occupies

### §5.5 — Priority Readings
- [A] Five sources: Romele et al., Phillips et al., Pence, Piotrowski, Hornby — preserve

---

## SECTION 6: Human-Centred AI Design — Christian Personalism and Technical Standards
**Estimated length:** 2,500–3,000 words  
**Source priority:** [A] substantially richer; [B] for metaphors  
**Function:** Translate philosophical principles into concrete architecture; the personalism → architecture bridge

### §6.1 — The AI-in-the-Loop Reframing

#### ¶6.1.1 — AI²L: the scholar controls, the agent assists
- [A] Natarajan et al. (2024, arXiv:2412.14232) — many "HITL" systems are actually AI-in-the-loop
- 🔑 KEY MOVE: "A religious studies research agent should be AI²L by design: the scholar is the controlling intelligence, the agent is an assistive instrument."
- [A] Not merely semantic — determines who initiates, who sets direction, where approval gates sit

#### ¶6.1.2 — Practical HITL implementations
- [A] ExtracTable (John et al., 2026) — LLMs + user-defined schemas for Open Research Knowledge Graph
- [A] AutoLit SLR system — 50% time savings in screening, 70-80% in qualitative extraction
- [A] CUNY "data ethics of care" — HITL connected to relational ethics and epistemic justice
- [NEW] Tuppal, C.P., et al. (2025). "Towards a Relational Understanding of Human Beings in an AI-Mediated World." *Scandinavian Journal of Caring Sciences* 39(3). DOI: 10.1111/scs.70097. — Three dimensions (relational ontology, ethical integration, philosophical foundations) for AI system design using hermeneutic methodology; directly supports the relational ontology → architecture translation in §6.3.2

### §6.2 — Graduated Autonomy for Religious Studies

#### ¶6.2.1 — The general taxonomy
- [A] Huang et al. (2025, Knight First Amendment Institute, Columbia) — L1 through L5:
  - L1 (Operator): User decides everything
  - L2 (Collaborator): Shared planning and execution
  - L3 (Consultant): Agent leads, consults user
  - L4 (Approver): Agent independent, seeks approval for high-risk
  - L5 (Observer): Full autonomy, user monitors only

#### ¶6.2.2 — Shneiderman's two-dimensional framework
- [A] Shneiderman (2020, 2022) — high automation AND high human control simultaneously
- [A] Design metaphors: Supertool, Control Centre, Active Appliance, Tele-operated device
- 🔑 KEY MOVE: A theological research agent = "Supertool with Control Centre oversight for sensitive interpretive tasks"

#### ¶6.2.3 — Domain-specific autonomy mapping (the novel contribution)
- [A] "No one has developed a task-specific autonomy mapping for religious studies"
- [A] Proposed mapping:
  - Bibliographic search: L3–L4
  - Source summarisation and metadata: L2–L3
  - Cross-reference identification: L2
  - Theological interpretation and hermeneutical synthesis: L1
  - Bias auditing and tradition identification: L2
- [B] Clean formulation: "Low Risk (Formatting bibliography): High Autonomy. High Risk (Translating a dogma): Low Autonomy (HITL required)."
- [NEW] Expand this table with specific examples from GNORM and ITSERR work packages

### §6.3 — Christian Personalism as Design Ethic

#### ¶6.3.1 — The Rome Call and its progeny
- [A] Rome Call for AI Ethics (2020) — six principles; expanded to all three Abrahamic faiths (2023)
- [A] Pope Leo XIV — "access to data must not be confused with intelligence"
- [A] Vatican 2025 *Linee Guida* — AI as "gift of human creativity, which itself is a gift from God"
- [A] TRUST framework (McGrath et al., 2025) — Theological alignment, Relational impact, Utility/justice, Stewardship, Transparency
- [A] Laracy, J.R., Kirova, V.D., Ku, C.S., & Marlowe, T.J. (2025). "Human Dignity and the Ethics of Artificial Intelligence: A Framework for Responsible Design and Use from the Perspective of Catholic Social Teaching." IEEE Conference Publication. 979-8-3315-3228-4/25. — Maps CST principles (human dignity, common good, solidarity, subsidiarity, stewardship) to UNESCO, IEEE, and IBM AI ethics frameworks; subsidiarity principle directly supports graduated autonomy design.
- [NEW] Fioravante, R. & Vaccaro, A. (2025). "Personalism in Generative AI Deployment: Deciding Ethically When Human Creative Expression is at Stake." *Humanistic Management Journal* 10: 387–409. DOI: 10.1007/s41463-024-00193-9. — Personalist framework (uniqueness, relationality, unpredictability) for ethical GAI deployment; directly relevant to the personalism → architecture translation.

#### ¶6.3.2 — The translation gap: from principle to architecture
- [A] "Yet the translation from principle to architecture remains unachieved"
- [A] The mapping proposal (this is the distinctive contribution):
  - **Relational ontology** → agent preserves researcher's interpretive narrative continuity
  - **Inviolable dignity** → agent never substitutes its "judgment" for researcher's on meaning questions
  - **Narrative constitution** → memory architecture tracks scholar's evolving story of understanding
  - **Subsidiarity** → decisions at most proximate level (scholar for interpretation, agent for retrieval)
- [B] "Subjectivity of Work" (John Paul II, *Laborem Exercens*) — "If an AI 'does the reading for us,' it robs the scholar of this subjective formation"
- [NEW] Fioravante, R. & Vaccaro, A. (2025). "Personalism in Generative AI Deployment." *Humanistic Management Journal* 10: 387–409. DOI: 10.1007/s41463-024-00193-9. — Personalist framework mapping uniqueness, relationality, and unpredictability to ethical GAI deployment; strengthens the personalism → architecture bridge with concrete deployment principles
- 🔑 KEY MOVE: This is the fourth major gap. Show it's not about applying ethics as a checklist but about deriving architecture from ontology.

#### ¶6.3.3 — Floridi's explicability as bridge
- [A] Floridi & Cowls (2019, *Harvard Data Science Review*) — five principles; the novel fifth: explicability (intelligibility + accountability)
- [A] Laitinen & Sahlgren (2021) — autonomy understood relationally, not merely individually
- [NEW] Show how Floridi's explicability maps to the "transparency over efficiency" principle in the prototype's tool system

### §6.4 — The Model Context Protocol as Relational Infrastructure

#### ¶6.4.1 — MCP: what it is and why it matters
- [A] Anthropic (Nov 2024); specification at modelcontextprotocol.io; adopted by OpenAI, Google, Microsoft; Linux Foundation; ~16,000 community servers
- [A] Core primitives: Tools, Resources, Prompts; JSON-RPC 2.0
- [B] "The Problem of Isolation: An LLM is an isolated brain in a jar. It knows only its training data."
- [B] "The Solution (Relationality): MCP allows the agent to connect to external Servers" — KEEP the metaphor
- [B] "The 'Vatican' Server" thought experiment — MCP server exposing read-only manuscript APIs
- [B] "Relational Ontology for the AI" — agent defined by its connections to authoritative sources

#### ¶6.4.2 — MCP for religious studies: no precedent
- [A] "MCP has not yet been applied to humanities research infrastructure" — this is the fifth gap (partially)
- [A] Sefaria MCP server as the closest model (Jewish texts)
- [A] Connecting to TLG, Patrologia, IxTheo would be genuinely novel
- [NEW] In the ITSERR context: MCP integration with GNORM, CRITERION, DaMSym, YASMINE

#### ¶6.4.3 — Security and trust considerations
- [B] Authentication, authorisation, leak prevention
- [A] Trust model: the agent's knowledge is grounded in its connections, not in open-web scraping
- [NEW] For sacred texts: the theological significance of *authoritative* sources vs. aggregated web data

---

## SECTION 7: European Research Infrastructure (2026 Status)
**Estimated length:** 1,500–2,000 words  
**Source priority:** [B] for V4 comparison; [A] for ITSERR/RESILIENCE detail  
**Function:** Map the institutional landscape; position Slovakia's opportunity

### §7.1 — RESILIENCE and ITSERR

#### ¶7.1.1 — RESILIENCE: ESFRI Roadmap to ERIC
- [A] ESFRI Roadmap 2021; Preparatory Phase (2022–2026); led by FSCIRE, Bologna
- [A] 13 partners, 11 countries; Financial Sustainability Plan; TNA Programme; IxTheo; RelReSearch
- [A] SSH Open Cluster connections (CESSDA, CLARIN, DARIAH, etc.)
- [A] Planned lifecycle: 4yr Preparatory → 8yr Implementation → 20yr Operation → 2yr Termination

#### ¶7.1.2 — ITSERR: the Italian national dimension
- [A] €22.1M; PNRR funded; CNR led; 5 universities
- [MERGE] Both cover work packages; use [A] for detail, [B] for summary table
- [A] WP3 (T-ReS: CRITERION + GNORM); WP4 (DaMSym); WP5 (Digital Maktaba); WP6 (YASMINE); WP8 (UbiQuity); WP9 (TAURUS)
- [A] UniPa contribution: 5 departments; Giorgio La Pira Library; Fondo Moncada Paternò
- 🔑 KEY MOVE: "ITSERR's tools await agentic integration — CRITERION, GNORM, DaMSym, and YASMINE are being developed as standalone tools rather than as components of an orchestrated AI agent workflow" — this is the fifth gap

### §7.2 — The V4 and CEE Landscape

#### ¶7.2.1 — Country profiles
- [B] Table 2 (European Digital Religious Infrastructure Comparison) — preserve and expand
- [B] Poland: Polona (4M+ objects); POLIN Jewish Heritage project
- [B] Czechia: Manuscriptorium (360,000+ records, 33M digitised pages); UNESCO Jikji Prize
- [B] Hungary: Hungaricana Portal (200,000 medieval documents); Czagány (2020) fragment research
- [B] Slovakia: Slovakiana; Bratislava Chapter Library codices; Cantus.sk
- [A] Tóth (2020) — scholarly overview of V4 digitisation

#### ¶7.2.2 — CEE religious heritage: fragmented but substantial
- [A] Slovakia: SND illuminated codices since 1995; Antiphonary of Bratislava II (UNESCO); Fragmentarium project (800+ medieval fragments); FamilySearch (1.6M Slovak church records)
- [A] Visegrad Fund "Mapping and Boosting Digital Humanities" project (digihum.cspk.eu)

### §7.3 — Slovakia's Position and the ELTF Opportunity [NEW]

#### ¶7.3.1 — The RESILIENCE Observer status pathway
- [NEW] Based on strategy documents and Cadeddu conversations
- Observer Agreement template; benefits (priority invitations, General Assembly attendance, open-source resources)
- Bologna General Assembly (May 11–12, 2026) as target event
- The ELTF pitch: Central European expertise, access to regional archives, UNESCO IRCAI connection

#### ¶7.3.2 — Infrastructure gaps as strategic opportunities
- [A] Five CEE-specific gaps:
  1. CEE underrepresentation in RESILIENCE (no V4 core partner)
  2. Protestant/Reformation heritage lacks dedicated digital infrastructure
  3. Non-Latin alphabet support underdeveloped (Church Slavonic, Old Hungarian)
  4. No unified CEE religious heritage portal
  5. ITSERR tools await agentic integration
- [NEW] Frame these not as complaints but as *contribution opportunities* — Slovakia brings something RESILIENCE currently lacks

---

## SECTION 8: Operational Roadmap for the TNA Fellowship [NEW]
**Estimated length:** 1,500–2,000 words  
**Source priority:** Drawn from strategy documents, palermo_preparation_briefing.md, reference_mapping.md  
**Function:** Transform the synthesis from reference document into working tool  
**Note:** Initial version now; update after Arianna meeting (Feb 12) with real specifics

### §8.1 — Prototype Architecture Decisions

#### ¶8.1.1 — Architecture following from the research
- [NEW] Synthesize: LangGraph for orchestration (§2.2); MemGPT-style hierarchical memory adapted for theology (§2.3); A-MEM Zettelkasten linking (§2.3); semantic entropy for factual claims (§3.2); four-tier epistemic classification (§3.2); HITL at interpretive decision points (§6.2); MCP for tool integration (§6.4)
- Reference existing codebase status from reference_mapping.md

#### ¶8.1.2 — Critical implementation priorities
- From reference_mapping.md gap analysis:
  - GNORM API verification (Week 1)
  - Concrete tool implementations (Week 2)
  - MCP protocol integration (Week 2)
  - User confirmation handlers (Week 3)

### §8.2 — Week-by-Week Plan

#### ¶8.2.1 — Week 1 (Feb 10–16): Orientation and listening
- Arianna meeting (Feb 12): GNORM API details, annotation workflow, philosophical questions
- WP4/WP6 team meetings
- Update `integrations/gnorm.py` with real endpoint information
- Priority reading: Sections 1 + 2 from this synthesis

#### ¶8.2.2 — Week 2 (Feb 17–23): Conceptual framework + prototyping
- Working paper draft: "Personalist Foundations for AI-Assisted Theological Research"
- Implement concrete tools, MCP integration
- Test against real GNORM API if available
- Circulate draft to hosts

#### ¶8.2.3 — Week 3 (Feb 24–27): Demonstration and documentation
- Feb 25 seminar: "Medieval hermeneutics and artificial intelligence" + Round table
- Consortium presentation preparation
- User confirmation handlers for HITL demonstration
- Final documentation with philosophical annotations

### §8.3 — Post-Fellowship Pipeline

#### ¶8.3.1 — Publication strategy
- Blog post (ITSERR website): March 2026
- Code repository public release: March 2026
- Faculty seminar (Comenius University): April 2026
- Conference presentation (DH2026 or European Academy): May–June 2026
- Journal article (*Open Theology* or *Religions*): June 2026
- Final results report: due late March 2026

#### ¶8.3.2 — Strategic next steps
- RESILIENCE Observer status follow-up (Cadeddu, Bologna)
- APVV grant outcome → Stöckel corpus scale decision
- GNORM adaptation pilot study design

---

## SECTION 9: Conclusion — Towards a Relational AI for Theology
**Estimated length:** 800–1,000 words  
**Source priority:** [A] five-gap convergence + [B] concluding points  
**Function:** Synthesize the argument; state the recommended architecture; frame the broader significance

### ¶9.1 — The convergence of five gaps
- [A] Full statement of the five-gap convergence (originally from Claude's conclusion):
  1. No agentic system for theological research
  2. Personalist anthropology never translated into architecture
  3. Protestant corpora computationally underserved
  4. Epistemic modesty for interpretive domains untheorised
  5. ITSERR tools await agentic orchestration
- 🔑 KEY MOVE: These gaps are not independent — they converge at a specific point that only someone with both theological hermeneutics expertise AND AI agent development skills can address

### ¶9.2 — The recommended prototype architecture
- [A] Comprehensive specification:
  - LangGraph for orchestration (graph = hermeneutical circle)
  - MemGPT/Letta memory adapted for theological research
  - A-MEM Zettelkasten linking
  - Semantic entropy for factual claims
  - Four-tier epistemic classification with explicit markers
  - HITL at all interpretive decision points (Shneiderman's Supertool-with-Control-Centre)
  - MCP for tool integration (ITSERR, IxTheo, scholarly databases)
- [NEW] Note: this architecture has no precedent — contribution to DH, AI agent research, and theological methodology simultaneously

### ¶9.3 — The broader significance
- [B] "We are moving from the *Digitization* of texts to the *Agentification* of research"
- [B] Four-point "clear path forward" (cleaned up):
  1. Architecture: LangGraph-based, stateful, graph-based control
  2. Philology: Hybrid approach (transformers + CRFs + 3D visualisation)
  3. Hermeneutics: Epistemic modesty; the agent refuses to feign Verstehen
  4. Ethics: Christian Personalism + MCP grounding in authoritative sources
- [NEW] Final sentence: not just technologically advanced but deeply human — an AI that respects both the sacredness of the text and the dignity of the person who reads it

---

## CONSOLIDATED BIBLIOGRAPHY (assembly instructions)

### Source handling
1. Start with all [A] citations (~142) — these have DOIs and full bibliographic entries
2. Add [B]-only citations, verifying each:
   - Replace blog post / Scribd citations with scholarly sources where possible
   - Retain only where content is unique and verifiable
   - Flag any citation lacking DOI or stable URL
3. Deduplicate across both sources
4. Standardise format: Author(s) (Year). "Title." *Journal/Venue* Volume(Issue): Pages. DOI.
5. Add any new sources from targeted searches (Search 1 and Search 2)

### New sources from targeted searches (Feb 13, 2026)
- Laracy, J.R., Kirova, V.D., Ku, C.S., & Marlowe, T.J. (2025). "Human Dignity and the Ethics of Artificial Intelligence." IEEE. 979-8-3315-3228-4/25.
- Fioravante, R. & Vaccaro, A. (2025). "Personalism in Generative AI Deployment." *Humanistic Management Journal* 10: 387–409. DOI: 10.1007/s41463-024-00193-9.
- Tuppal, C.P., Tuppal, S.M., Tuppal, S.M., & Ninobla, M.M. (2025). "Towards a Relational Understanding of Human Beings in an AI-Mediated World: A Hermeneutical Reading." *Scandinavian Journal of Caring Sciences* 39(3). DOI: 10.1111/scs.70097.
- Li, Z. & Wu, Q. (2025). "Let It Go or Control It All? The Dilemma of Prompt Engineering in Generative Agent-Based Models." *System Dynamics Review* 41(3). DOI: 10.1002/sdr.70008. — Four-component analysis (profile, memory, planning, action); over-control vs. authenticity dilemma directly relevant to §2.3 (narrative memory) and §6.2 (graduated autonomy).
- Jenkins, D.M., Cleverley-Thompson, S., Erikson, D., Blankenbaker, A., & Brown-Saracino, B. (2025). "Prompting for Meaning: Exploring Generative AI Tools for Qualitative Data Analysis in Leadership Research." *Journal of Leadership Studies* 19(3). DOI: 10.1002/jls.70014. — Introduces "epistemic friction" concept; GenAI for qualitative coding with human oversight for interpretive depth. Candidate for §3.

### Search notes (Feb 13, 2026)
Two additional Scholar Gateway searches (epistemic uncertainty in interpretive domains; DH agentic workflows) confirmed rather than filled the gap: no peer-reviewed work applies agentic AI to humanities or theological research. This strengthens Gap 1 in the five-gap convergence analysis.

### Estimated final count: ~150–160 unique sources

---

## CROSS-REFERENCE MAP: Where the Five Gaps Appear

| Gap | First introduced | Developed | Operational implication |
|-----|-----------------|-----------|----------------------|
| 1. No agentic system for theology | §1 (¶1.4) | §2 (§2.4) | §8 (§8.1) |
| 2. Personalism → architecture gap | §1 (¶1.4) | §6 (§6.3.2) | §8 (§8.1) |
| 3. Protestant corpus gap | §1 (¶1.4) | §4 (§4.2.3) | §8 (§8.2) |
| 4. Epistemic modesty for interpretation | §1 (¶1.4) | §3 (§3.2) | §8 (§8.1) |
| 5. ITSERR tools await agentic orchestration | §1 (¶1.4) | §7 (§7.1.2) | §8 (§8.2) |

---

*This outline is the final Phase 1 deliverable. Phase 2 begins with Search 1, then drafting Sections 2, 3, and 6.*

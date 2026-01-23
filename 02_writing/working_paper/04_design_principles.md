# Section 4: Design Principles — From Philosophy to Architecture

## 4.1 Introduction

The philosophical framework articulated in Section 2 and the engagement typology of Section 3 must now be translated into concrete design principles. This section presents three core innovations that operationalize personalist values in AI system architecture.

## 4.2 Principle 1: Narrative Memory System

### Philosophical Grounding

The personalist emphasis on the person as a *narrative* being—one whose identity unfolds through time, shaped by memory and anticipation—grounds our first design principle. The researcher is not a series of discrete queries but a person engaged in an ongoing hermeneutical journey.

Ricoeur's concept of *narrative identity* is instructive: we understand ourselves through the stories we tell about our engagement with texts, traditions, and questions. An AI assistant that treats each interaction as isolated fragments this narrative, undermining the continuity essential to deep research.

### Design Response: Three Memory Streams

We implement narrative continuity through three distinct memory streams:

| Stream | Purpose | Retention | Example |
|--------|---------|-----------|---------|
| **Conversation** | Recent exchanges, clarifications | High recency weight | "What's your take on Gadamer's hermeneutical circle?" |
| **Research** | Sources consulted, notes created | Long-term, relevance-weighted | "Consulted Ricoeur's *Time and Narrative*, pp. 52-89" |
| **Decision** | Methodological and interpretive choices | Preserved indefinitely | "Decided to focus on Romantic hermeneutics over medieval" |

### Technical Implementation

- **Vector store**: ChromaDB for semantic retrieval with metadata tracking
- **Embeddings**: Local sentence-transformers (all-MiniLM-L6-v2) for privacy
- **Retrieval**: Top-k similarity with stream-type filtering and recency weighting
- **Reflection**: Periodic summarization to prevent context overflow while preserving narrative essence

### Alignment with Personalist Values

The three-stream architecture respects:
- **Temporal continuity**: The researcher's journey unfolds across sessions
- **Contextual sensitivity**: Current questions are informed by past exploration
- **Decision preservation**: Methodological choices are remembered, not re-litigated

## 4.3 Principle 2: Epistemic Modesty Indicators

### Philosophical Grounding

The personalist commitment to honesty and respect for the other demands that AI systems not misrepresent their epistemic status. When an AI presents an interpretation as fact, it deceives the researcher and undermines their agency.

Buber's I-Thou ethic requires treating the researcher as a genuine dialogue partner, not someone to be managed through confident-sounding but epistemically uncertain assertions.

### Design Response: Tripartite Classification

Every AI response is classified using three indicators:

```
┌─────────────────────────────────────────────────────────────────┐
│    [FACTUAL]        [INTERPRETIVE]        [DEFERRED]            │
│                                                                  │
│    Verifiable       AI-assisted           Requires human        │
│    information      synthesis             judgment              │
│                                                                  │
│    High confidence  Medium confidence     Beyond AI             │
│    Source-backed    Pattern-based         competence            │
│    Checkable        Should be verified    Researcher decides    │
└─────────────────────────────────────────────────────────────────┘
```

### Classification Rules

**[FACTUAL]** triggers:
- Citations present (author, date, page)
- Historical dates with scholarly consensus
- Direct quotations from sources
- Quantitative textual data

**[INTERPRETIVE]** triggers:
- Hedge words: "suggests," "appears," "may indicate"
- Pattern language: "connection," "echoes," "structure"
- Comparative analysis
- Synthetic observations

**[DEFERRED]** triggers:
- Theological truth claims
- Normative language: "should," "must," "better"
- Questions of meaning and significance
- Evaluative judgments

### Technical Implementation

- **Dual-layer classification**: LLM-level (system prompt instructs indicator use) + Classifier-level (rule-based validation and tagging)
- **Confidence thresholds**: High (≥0.85) → FACTUAL eligible; Medium → INTERPRETIVE; Low → flag for review
- **Redundant validation (dual-layer check)**: Classifier validates LLM-added tags and adds missing ones

### Alignment with Personalist Values

- **Honesty**: The AI does not claim more than it knows
- **Agency preservation**: Researcher knows what requires their judgment
- **Dialogue**: Epistemic status is transparent, enabling genuine exchange

## 4.4 Principle 3: Human-Centered Tool Patterns

### Philosophical Grounding

Wojtyla's concept of the *acting person* emphasizes self-determination—the capacity to be the author of one's own acts. In AI-assisted research, this means the scholar must remain in control of actions that affect their research artifacts.

A system that silently modifies files, sends queries to external services, or makes decisions without researcher awareness violates this principle.

### Design Response: Confirmation Gates

Tools are categorized by their impact, with confirmation requirements scaled accordingly:

| Category | Confirmation | Examples |
|----------|--------------|----------|
| **Read-only** | None (auto-execute) | Search, memory retrieval, lookups |
| **Note-taking** | Optional | Create notes, add annotations |
| **Modification** | Explicit required | File operations, edits |
| **External** | Confirmation + first-time gate | GNORM API calls, T-ReS queries |

### Technical Implementation

- **Tool registry**: Central registry with metadata (category, description, confirmation requirements)
- **Execution gate**: Checks category before execution, prompts user if required
- **First-use gate**: External services require explicit acknowledgment on first use
- **Audit trail**: All tool invocations logged with timestamps and outcomes

### Alignment with Personalist Values

- **Self-determination**: Researcher controls what happens to their work
- **Transparency**: No hidden actions or side effects
- **Trust**: Researcher can rely on the system to respect boundaries

## 4.5 Integration: How the Principles Work Together

The three principles are not independent but mutually reinforcing:

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER QUERY                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              NARRATIVE MEMORY RETRIEVAL                          │
│    "What has this researcher been exploring?"                    │
│    → Informs response with narrative context                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              RESPONSE GENERATION                                 │
│    LLM generates response with epistemic indicators              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              EPISTEMIC CLASSIFICATION                            │
│    Classifier validates/adds [FACTUAL]/[INTERPRETIVE]/[DEFERRED] │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              TOOL EXECUTION (if needed)                          │
│    Human-centered confirmation gates                             │
│    → GNORM annotation, file operations, etc.                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              MEMORY UPDATE                                       │
│    Store exchange in narrative memory                            │
│    Trigger reflection if threshold reached                       │
└─────────────────────────────────────────────────────────────────┘
```

## 4.6 Design Trade-offs

Honest engineering requires acknowledging trade-offs:

| Principle | Benefit | Cost |
|-----------|---------|------|
| Narrative memory | Contextual continuity | Increased complexity, storage needs |
| Epistemic indicators | Transparent epistemic status | Some response overhead, learning curve |
| Confirmation gates | User control | Slower interaction for some operations |

We argue these costs are justified for scholarly research where accuracy and agency matter more than speed.

---

## Notes for Revision

- [ ] Add specific code examples for each principle
- [ ] Discuss failure modes and mitigation
- [ ] Compare to other approaches (e.g., RAG without narrative framing)
- [ ] Address scalability concerns for narrative memory
- [ ] Include user feedback from prototype testing

---

**Word Count Target:** 1200-1500 words
**Current Draft:** ~1000 words (structured outline)

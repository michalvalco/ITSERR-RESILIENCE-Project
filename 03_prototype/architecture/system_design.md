# System Design: Ethically-Grounded AI Agent for Religious Studies

## Overview

This document describes the architecture for an AI research assistant prototype designed to support theological and religious studies scholarship while maintaining epistemic humility and human agency.

**Version:** 0.1 (Pre-Fellowship Draft)
**Last Updated:** [Date]
**Status:** Initial architecture—to be refined during GNORM technical briefing

---

## Design Philosophy

The architecture is guided by three principles derived from personalist anthropology:

1. **Narrative Continuity**: Preserve the researcher's hermeneutical journey across sessions
2. **Epistemic Modesty**: Clearly differentiate what the AI knows vs. interprets vs. cannot determine
3. **Human Agency**: Keep the researcher in control of all significant actions

These principles map to three core technical innovations.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                     (CLI / IDE Integration / Web UI)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENT ORCHESTRATOR                                 │
│                         (LangGraph / LangChain)                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │   Input Parser  │  │ Response Router │  │   Epistemic Classifier      │  │
│  │                 │  │                 │  │   [FACTUAL/INTERPRETIVE/    │  │
│  │ - Query analysis│  │ - Tool dispatch │  │    DEFERRED]                │  │
│  │ - Intent detect │  │ - Memory lookup │  │                             │  │
│  │ - Context merge │  │ - Output format │  │                             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
          │                       │                         │
          ▼                       ▼                         ▼
┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────────────┐
│  NARRATIVE       │  │  TOOL            │  │  EXTERNAL INTEGRATIONS        │
│  MEMORY SYSTEM   │  │  REGISTRY        │  │                               │
│                  │  │                  │  │  ┌─────────────────────────┐  │
│  ┌────────────┐  │  │  - Search tools  │  │  │ GNORM API               │  │
│  │ ChromaDB   │  │  │  - Citation      │  │  │ (CRF annotations)       │  │
│  │ (Vector    │  │  │    lookup        │  │  └─────────────────────────┘  │
│  │  Store)    │  │  │  - Note creation │  │  ┌─────────────────────────┐  │
│  └────────────┘  │  │  - File ops      │  │  │ T-ReS Integration       │  │
│  ┌────────────┐  │  │  - GNORM/T-ReS   │  │  │ (Text analysis)         │  │
│  │ Session    │  │  │    integration   │  │  └─────────────────────────┘  │
│  │ Index      │  │  │                  │  │  ┌─────────────────────────┐  │
│  └────────────┘  │  │  MCP Protocol    │  │  │ Reference DBs           │  │
│  ┌────────────┐  │  │  for tool calls  │  │  │ (Citations, sources)    │  │
│  │ Reflection │  │  │                  │  │  └─────────────────────────┘  │
│  │ Summaries  │  │  │                  │  │                               │
│  └────────────┘  │  │                  │  │                               │
└──────────────────┘  └──────────────────┘  └───────────────────────────────┘
```

---

## Component Details

### 1. Narrative Memory System

**Purpose:** Maintain contextual continuity across research sessions, preserving the researcher's hermeneutical journey.

**Architecture:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    NARRATIVE MEMORY SYSTEM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    MEMORY STREAMS                         │   │
│  │                                                           │   │
│  │  Conversation Stream    Research Stream    Decision Stream│   │
│  │  ─────────────────     ──────────────     ───────────────│   │
│  │  Recent exchanges      Sources consulted  Choices made   │   │
│  │  Questions asked       Notes created      Paths taken    │   │
│  │  Clarifications        Annotations        Alternatives   │   │
│  │                                           rejected       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   VECTOR STORE (ChromaDB)                 │   │
│  │                                                           │   │
│  │  - Semantic embeddings of all memory items                │   │
│  │  - Metadata: timestamp, session_id, memory_type, source   │   │
│  │  - Similarity search for context retrieval                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  REFLECTION LAYER                         │   │
│  │                                                           │   │
│  │  Periodic summarization:                                  │   │
│  │  - "What questions has the researcher been exploring?"    │   │
│  │  - "What interpretive positions have emerged?"            │   │
│  │  - "What sources have been most influential?"             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Design Decisions:**

| Decision | Rationale |
|----------|-----------|
| Three separate streams | Different retention and retrieval needs |
| ChromaDB for vectors | Lightweight, local-first, good Python integration |
| Reflection summaries | Prevents context window overflow while preserving continuity |
| Session isolation | Each research project maintains distinct memory |

**Implementation Notes:**

- Embedding model: `text-embedding-3-small` (OpenAI) or `all-MiniLM-L6-v2` (local)
- Retrieval: Top-k similarity with recency weighting
- Summarization trigger: Every N exchanges or on session close

---

### 2. Epistemic Modesty Indicators

**Purpose:** Clearly differentiate response types to prevent false certainty about interpretive matters.

**Indicator Taxonomy:**

```
┌─────────────────────────────────────────────────────────────────┐
│                  EPISTEMIC INDICATOR SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [FACTUAL]                                                       │
│  ─────────                                                       │
│  Verifiable information that can be checked against sources      │
│                                                                  │
│  Examples:                                                       │
│  - Dates, names, bibliographic data                              │
│  - Direct quotations with citations                              │
│  - Definition of terms (from specified source)                   │
│  - Historical events (with scholarly consensus)                  │
│                                                                  │
│  Signal: High confidence, can be verified                        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [INTERPRETIVE]                                                  │
│  ──────────────                                                  │
│  AI-assisted analysis involving pattern recognition, synthesis   │
│                                                                  │
│  Examples:                                                       │
│  - Connections between texts/concepts                            │
│  - Thematic patterns across sources                              │
│  - Structural analysis of arguments                              │
│  - Comparative observations                                      │
│                                                                  │
│  Signal: AI contribution, should be verified by researcher       │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [DEFERRED]                                                      │
│  ──────────                                                      │
│  Matters requiring human judgment that AI cannot determine       │
│                                                                  │
│  Examples:                                                       │
│  - Theological truth claims                                      │
│  - Value judgments about religious practices                     │
│  - "Correct" interpretation of contested passages                │
│  - Assessment of spiritual significance                          │
│                                                                  │
│  Signal: Explicitly beyond AI competence, researcher decides     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Classification Pipeline:**

```
User Query → Content Analysis → Classification → Tagged Response
                   │
                   ▼
        ┌─────────────────────────────────────┐
        │     CLASSIFICATION HEURISTICS        │
        │                                      │
        │  1. Source attribution check         │
        │     - Has citation? → FACTUAL        │
        │     - Verifiable date/name? → FACTUAL│
        │                                      │
        │  2. Interpretive markers             │
        │     - "suggests", "pattern" → INTERP │
        │     - "connection", "theme" → INTERP │
        │                                      │
        │  3. Normative/theological content    │
        │     - Truth claims → DEFERRED        │
        │     - Value judgments → DEFERRED     │
        │     - "should", "correct" → DEFERRED │
        │                                      │
        │  4. Uncertainty detection            │
        │     - Low confidence → Flag          │
        │     - Contested topic → Flag         │
        └─────────────────────────────────────┘
```

**Implementation Approach:**

- Prompt engineering: System prompt includes indicator definitions and examples
- Post-processing: Regex/heuristic check to ensure indicators present
- Fallback: If uncertain, default to `[INTERPRETIVE]` or `[DEFERRED]`

---

### 3. Human-Centered Tool-Calling Patterns

**Purpose:** Maintain researcher agency through transparent, confirmable tool invocations.

**Tool Categories:**

| Category | Examples | Confirmation Required |
|----------|----------|----------------------|
| **Read-only** | Search, lookup, retrieve | No |
| **Note-taking** | Create note, add annotation | Optional |
| **Modification** | Edit file, update citation | Yes |
| **External** | GNORM API, T-ReS query | Yes (first time) |

**Tool Interaction Flow:**

```
                    ┌─────────────────────────┐
                    │     User Request        │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   Tool Selection        │
                    │   (Agent reasoning)     │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │  Confirmation Check     │
                    │  (Based on category)    │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ Auto-execute    │ │ Show intent,    │ │ Explicit        │
    │ (read-only)     │ │ proceed unless  │ │ confirmation    │
    │                 │ │ user stops      │ │ required        │
    └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
             │                   │                   │
             └───────────────────┴───────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   Tool Execution        │
                    │   (with logging)        │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   Result Presentation   │
                    │   (transparent output)  │
                    └─────────────────────────┘
```

**Transparency Features:**

1. **Pre-execution disclosure**: "I'm going to search GNORM for annotations on [text]"
2. **Tool call visibility**: User can see what tools are being invoked
3. **Result explanation**: "I found 3 relevant annotations. Here's what they show..."
4. **Override mechanism**: User can cancel, modify, or redirect at any point

---

## Data Flow

### Typical Interaction Sequence

```
1. User: "What does Gadamer say about the hermeneutical circle?"

2. Agent Orchestrator:
   - Parse intent: factual lookup
   - Check memory: any prior Gadamer discussions?
   - Select tools: search + citation lookup

3. Memory System:
   - Retrieve: previous session discussed Gadamer pp. 268-270
   - Add context to query

4. Tool Execution:
   - Search bibliography for Gadamer sources
   - Retrieve relevant passages

5. Epistemic Classification:
   - Direct quote → [FACTUAL]
   - Researcher's previous notes → [FACTUAL] (attributed)
   - Pattern connection → [INTERPRETIVE]

6. Response Assembly:
   "[FACTUAL] Gadamer defines the hermeneutical circle as..."
   "[FACTUAL] In your previous session, you noted that..."
   "[INTERPRETIVE] This connects to your interest in..."

7. Memory Update:
   - Store: new conversation entry
   - Index: semantic embedding for future retrieval
```

---

## Integration Points

### GNORM Integration (WP3)

```
┌─────────────────────────────────────────────────────────────────┐
│                      GNORM INTEGRATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Agent                        GNORM API                          │
│    │                             │                               │
│    │  1. Request annotations     │                               │
│    │  ─────────────────────────► │                               │
│    │     {text_id, entity_types} │                               │
│    │                             │                               │
│    │  2. Return CRF annotations  │                               │
│    │  ◄───────────────────────── │                               │
│    │     {entities, relations,   │                               │
│    │      confidence_scores}     │                               │
│    │                             │                               │
│    │  3. Present with indicators │                               │
│    │     [FACTUAL] for high-conf │                               │
│    │     [INTERPRETIVE] for low  │                               │
│    │                             │                               │
└─────────────────────────────────────────────────────────────────┘

Key Integration Questions (for WP3 briefing):
- API format and authentication
- Available entity types for religious texts
- Confidence score interpretation
- Batch vs. real-time processing
```

### T-ReS Integration (WP3)

- Text analysis workflows
- Annotation sharing format
- Complementary tool capabilities

### Future Integrations

- **WP4 (DaMSym)**: Semantic analysis for memory indexing
- **WP6 (YASMINE)**: Ethical guidelines enforcement
- **WP7 (REVER)**: Hermeneutical tradition patterns

---

## Technical Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Agent Framework | LangChain / LangGraph | Mature, flexible, good tool support |
| Tool Protocol | Model Context Protocol (MCP) | Standardized tool integration |
| Vector Store | ChromaDB | Local-first, Python-native, lightweight |
| Embedding | OpenAI / local model | Flexible deployment options |
| LLM | Claude / GPT-4 | Strong reasoning, good instruction following |
| Language | Python 3.11+ | Ecosystem compatibility |

---

## Development Phases

### Phase 1: Core Agent (Week 2)
- Basic LangChain agent setup
- Simple memory (conversation buffer)
- Tool registry with 3-4 tools

### Phase 2: Memory System (Week 2)
- ChromaDB integration
- Memory streams implementation
- Basic reflection

### Phase 3: Epistemic Indicators (Week 2-3)
- Classification pipeline
- Response formatting
- Indicator validation

### Phase 4: GNORM Integration (Week 3)
- API integration
- Annotation display
- Confidence mapping

---

## Open Questions

To be resolved during fellowship:

1. **Memory persistence**: Local files vs. cloud storage for cross-device access?
2. **GNORM API**: Real-time or batch processing? Authentication model?
3. **Indicator granularity**: Sentence-level or paragraph-level tagging?
4. **Tool confirmation**: How intrusive should confirmation dialogs be?
5. **Deployment**: Local-only prototype or hosted demo for presentation?

---

## Success Criteria

The prototype succeeds if it demonstrates:

- [ ] Memory retrieval from previous sessions that meaningfully informs responses
- [ ] Consistent epistemic indicator usage across response types
- [ ] Transparent tool invocation with user control
- [ ] At least one working GNORM integration example
- [ ] Clear philosophical-technical mappings in code comments

---

*This document will be updated after the GNORM technical briefing (Feb 11-12).*

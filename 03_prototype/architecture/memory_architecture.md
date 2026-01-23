# Narrative Memory System: Architecture Detail

**Status:** Implementation Guide
**References:** `system_design.md` Section 3.1
**Implementation:** `src/itserr_agent/memory/`

---

## Overview

The Narrative Memory System maintains contextual continuity across research sessions, preserving the researcher's hermeneutical journey rather than just isolated data points. This document provides implementation details expanding on the system design.

---

## Design Philosophy

Traditional AI memory systems focus on information retrieval. Our approach is fundamentally different:

> **We preserve the narrative of inquiry, not just the facts discovered.**

This means tracking:
- What questions drove the researcher
- How understanding evolved through dialogue
- Which interpretive choices were made and why
- What sources proved most influential

This design reflects the personalist anthropology informing the ITSERR project—the researcher is not merely extracting information but engaging in a hermeneutical process that shapes their understanding.

---

## Three-Stream Architecture

### Stream 1: Conversation Stream

**Purpose:** Capture the immediate dialogue flow and clarifications.

**Characteristics:**
- High recency weight in retrieval
- Shorter retention (summarized after N exchanges)
- Captures questioning patterns and clarification needs

**Data Structure:**
```python
@dataclass
class ConversationMemory:
    user_input: str
    agent_response: str
    timestamp: datetime
    session_id: str

    # Derived metadata
    question_type: str | None  # factual, interpretive, methodological
    clarification_count: int
    topic_tags: list[str]
```

**Retention Policy:**
- Recent 10 exchanges: Full retention
- Exchanges 11-50: Compressed to key points
- Older: Summarized into "session themes"

**Why This Matters:**
The conversation stream helps the agent understand *how* the researcher thinks and asks questions, not just what they ask. A researcher who frequently seeks clarification on theological terminology should receive more proactive definitions.

---

### Stream 2: Research Stream

**Purpose:** Track scholarly engagement—sources consulted, annotations created, notes taken.

**Characteristics:**
- High relevance weight in retrieval
- Long retention (preserved across sessions)
- Captures scholarly engagement patterns

**Data Structure:**
```python
@dataclass
class ResearchMemory:
    content: str
    source_type: str  # citation, annotation, note, quote
    source_reference: str | None  # bibliographic reference
    timestamp: datetime
    session_id: str

    # Scholarly metadata
    author: str | None
    work_title: str | None
    page_reference: str | None
    user_annotation: str | None
```

**Retention Policy:**
- All research items retained indefinitely
- Periodic consolidation (linking related items)
- Source popularity tracking

**Why This Matters:**
A researcher who has extensively annotated Gadamer should have that context readily available when discussing hermeneutics, even months later. The research stream creates a "scholarly profile" of the inquiry.

---

### Stream 3: Decision Stream

**Purpose:** Record methodological and interpretive choices made during research.

**Characteristics:**
- Preserved long-term
- Captures reasoning and rejected alternatives
- Enables reflection on research direction

**Data Structure:**
```python
@dataclass
class DecisionMemory:
    decision: str
    rationale: str
    alternatives_considered: list[str]
    timestamp: datetime
    session_id: str

    # Decision metadata
    decision_type: str  # methodological, interpretive, scope
    confidence: float
    reversible: bool
```

**Retention Policy:**
- All decisions retained indefinitely
- Decision chains tracked (how one decision influenced others)
- Periodic "decision audit" prompts

**Why This Matters:**
When a researcher returns to a project after weeks, the decision stream reminds them *why* they chose a particular interpretive approach. This prevents repetitive exploration of already-rejected paths.

---

## Vector Store Implementation

### ChromaDB Configuration

```python
# Collection settings
COLLECTION_CONFIG = {
    "name": "itserr_memory",
    "metadata": {
        "hnsw:space": "cosine",  # Cosine similarity for semantic search
        "hnsw:construction_ef": 100,  # Build quality
        "hnsw:search_ef": 50,  # Search quality
    }
}

# Document metadata schema
METADATA_SCHEMA = {
    "stream_type": str,     # conversation, research, decision
    "session_id": str,      # Research project identifier
    "timestamp": str,       # ISO format
    "recency_weight": float,  # Decay factor for retrieval
}
```

### Embedding Strategy

**Primary Option:** Local embeddings with `sentence-transformers`
```python
model = SentenceTransformer("all-MiniLM-L6-v2")
# 384-dimension embeddings
# Fast inference, no API costs
# Good performance on academic text
```

**Alternative:** OpenAI embeddings for higher quality
```python
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# 1536-dimension embeddings
# Higher quality, API cost
# Better for nuanced theological terminology
```

**Recommendation:** Start with local embeddings for development, benchmark against OpenAI for production decision.

---

## Retrieval Algorithm

### Recency-Weighted Semantic Search

Standard semantic search returns the most similar items. Our approach weights by both relevance *and* recency:

```python
def retrieve_context(query: str, top_k: int = 5) -> list[MemoryItem]:
    # 1. Get semantic candidates (more than needed)
    candidates = vector_store.similarity_search(query, k=top_k * 3)

    # 2. Calculate combined score
    scored = []
    for item in candidates:
        semantic_score = item.similarity  # 0-1
        recency_score = calculate_recency(item.timestamp)  # 0-1, decays

        # Stream-specific weights
        weights = STREAM_WEIGHTS[item.stream_type]
        combined = (
            semantic_score * weights.semantic +
            recency_score * weights.recency
        )
        scored.append((item, combined))

    # 3. Return top-k by combined score
    scored.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in scored[:top_k]]
```

### Stream-Specific Weights

| Stream | Semantic Weight | Recency Weight | Rationale |
|--------|-----------------|----------------|-----------|
| Conversation | 0.5 | 0.5 | Recent dialogue context matters |
| Research | 0.8 | 0.2 | Scholarly sources remain relevant |
| Decision | 0.7 | 0.3 | Past decisions inform current work |

---

## Reflection Layer

### Purpose

Prevent context window overflow while preserving narrative continuity. Periodically summarize and compress older memories.

### Trigger Conditions

1. **Exchange count:** Every 10 conversation exchanges
2. **Session close:** When a session ends
3. **Memory size:** When conversation stream exceeds threshold

### Reflection Prompts

The reflection layer uses the LLM to generate summaries:

```python
REFLECTION_PROMPTS = {
    "questions": """
    Review the recent exchanges and summarize:
    - What questions has the researcher been exploring?
    - What patterns do you see in their inquiry?
    - What remains unresolved?

    Be concise (2-3 sentences).
    """,

    "positions": """
    Based on recent discussions, what interpretive positions
    has the researcher been developing? Note any shifts or
    refinements in their thinking.
    """,

    "sources": """
    Which sources have been most influential in recent
    discussions? What aspects of these sources have
    received the most attention?
    """,
}
```

### Reflection Storage

Reflections are stored as special memory items:
```python
@dataclass
class ReflectionMemory:
    reflection_type: str  # questions, positions, sources
    content: str
    covered_period: tuple[datetime, datetime]
    exchange_count: int
    timestamp: datetime
```

---

## Session Isolation

### Why Isolation?

A researcher may work on multiple projects (e.g., dissertation chapter on Gadamer, article on Ricoeur). Cross-contamination of memory between projects would create confusion.

### Implementation

```python
# Session ID format
session_id = f"{project_name}_{user_id}_{created_date}"

# Query with session filter
results = collection.query(
    query_embeddings=[embedding],
    where={"session_id": session_id},
    n_results=5
)
```

### Cross-Session Search

Optionally allow searching across sessions (e.g., "Have I discussed this author in other projects?"):

```python
def cross_session_search(query: str, sessions: list[str] | None = None):
    where_filter = {"session_id": {"$in": sessions}} if sessions else None
    return collection.query(
        query_embeddings=[embed(query)],
        where=where_filter,
        n_results=10
    )
```

---

## Data Flow Example

### Scenario: Continuing Previous Research

```
1. User: "What did I conclude about Gadamer's concept of horizon?"

2. Agent receives query, triggers memory retrieval:
   - Query embedding generated
   - Search across all streams with recency weighting

3. Memory System returns:
   - [RESEARCH] Note from 3 days ago: "Gadamer pp. 268-270 on
     horizon fusion - key for my hermeneutical approach"
   - [CONVERSATION] From yesterday: discussion of horizon vs.
     Ricoeur's distanciation
   - [DECISION] 5 days ago: "Adopting Gadamer's horizon language
     rather than Ricoeur's for consistency"

4. Agent response incorporates context:
   "[FACTUAL] In your previous session, you noted that Gadamer's
   concept of horizon (Truth and Method, pp. 268-270) was key to
   your hermeneutical approach. [INTERPRETIVE] You also made a
   methodological decision to use Gadamer's terminology rather
   than Ricoeur's concept of distanciation for consistency."
```

---

## Performance Considerations

### Embedding Latency

| Operation | Local (MiniLM) | OpenAI API |
|-----------|----------------|------------|
| Single embed | ~10ms | ~200ms |
| Batch (10) | ~50ms | ~300ms |

**Recommendation:** Batch embeddings where possible.

### ChromaDB Limits

- Collection size: Tested to 1M documents
- Query latency: <50ms for 100k documents
- Memory: ~1GB per 100k documents (with embeddings)

### Optimization Strategies

1. **Lazy embedding:** Only embed when adding to long-term memory
2. **Embedding cache:** Cache embeddings for frequently-queried items
3. **Hierarchical retrieval:** First filter by session/stream, then semantic search

---

## Implementation Checklist

- [ ] ChromaDB collection setup with proper metadata schema
- [ ] Three stream classes with appropriate data structures
- [ ] Embedding function with local/OpenAI toggle
- [ ] Recency-weighted retrieval algorithm
- [ ] Reflection trigger logic
- [ ] Session isolation and cross-session search
- [ ] Memory persistence and recovery

---

## Open Questions

1. **Embedding model:** Final decision on local vs. OpenAI for production
2. **Reflection frequency:** Optimal exchange count for triggering reflection
3. **Cross-project memory:** How much should projects share common knowledge?
4. **Privacy:** How to handle memory export/deletion requests?

---

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [Sentence Transformers](https://www.sbert.net/)
- `system_design.md` - Parent architecture document

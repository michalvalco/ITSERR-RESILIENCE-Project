# Section 5: From Principles to Implementation

## 5.1 Introduction

This section presents the concrete implementation of the design principles articulated in Section 4. We describe the ITSERR Agent prototype, its architecture, and its integration with the GNORM digital humanities infrastructure.

## 5.2 System Architecture Overview

The implementation follows a layered architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                   COMMAND LINE INTERFACE                         │
│                        (Typer/Rich)                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENT ORCHESTRATOR                             │
│                    (ITSERRAgent)                                 │
│         LangChain/LangGraph for conversation management          │
└─────────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  MEMORY SYSTEM   │ │    EPISTEMIC     │ │  TOOL REGISTRY   │
│                  │ │   CLASSIFIER     │ │                  │
│  - Conversation  │ │                  │ │  - GNORM Client  │
│  - Research      │ │  - Rule-based    │ │  - File Ops      │
│  - Decision      │ │  - Confidence    │ │  - Search        │
│                  │ │    thresholds    │ │                  │
│  ChromaDB        │ │                  │ │  Confirmation    │
│  + Embeddings    │ │                  │ │  Gates           │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

## 5.3 Core Components

### 5.3.1 ITSERRAgent (core/agent.py)

The main orchestrator coordinates the agent's reasoning loop:

```python
class ITSERRAgent:
    """
    Ethically-grounded AI agent for religious studies research.

    Implements three core innovations:
    1. Narrative Memory System
    2. Epistemic Modesty Indicators
    3. Human-Centered Tool Patterns
    """

    async def process(self, user_input: str, session_id: str | None = None):
        # 1. Retrieve narrative context
        memory_context = await self._memory.retrieve_context(query=user_input)

        # 2. Generate response with LLM
        response = await self._llm.ainvoke(self._build_messages(user_input, memory_context))

        # 3. Classify with epistemic indicators
        tagged_response = self._classifier.classify_and_tag(response.content)

        # 4. Store in narrative memory
        await self._memory.store_exchange(user_input, tagged_response, session_id)

        return AIMessage(content=tagged_response)
```

### 5.3.2 Narrative Memory System (memory/narrative.py)

The memory system implements the three-stream architecture:

```python
class NarrativeMemorySystem:
    """Maintains contextual continuity across research sessions."""

    def __init__(self, config: AgentConfig):
        self._conversation = ConversationStream()
        self._research = ResearchStream()
        self._decision = DecisionStream()
        self._initialize_storage()  # ChromaDB

    async def retrieve_context(self, query: str, session_id: str | None = None):
        """Semantic retrieval with stream-type metadata."""
        # Vector similarity search with recency weighting

    async def store_exchange(self, user_input: str, agent_response: str, session_id: str | None):
        """Store conversation exchange and check reflection trigger."""

    async def _trigger_reflection(self, session_id: str | None):
        """Generate periodic summaries to prevent context overflow."""
```

### 5.3.3 Epistemic Classifier (epistemic/classifier.py)

The classifier implements the indicator framework:

```python
class EpistemicClassifier:
    """Rule-based epistemic classification with LLM validation."""

    def classify_and_tag(self, content: str) -> str:
        """Add epistemic indicators to response content."""
        sentences = self._split_sentences(content)
        tagged = []

        for sentence in sentences:
            if self._already_tagged(sentence):
                tagged.append(sentence)  # Preserve LLM-added tags
            else:
                indicator = self._classify_sentence(sentence)
                tagged.append(f"[{indicator.value}] {sentence}")

        return " ".join(tagged)

    def _classify_sentence(self, sentence: str) -> EpistemicIndicator:
        """Apply classification rules."""
        if self._has_citation(sentence):
            return EpistemicIndicator.FACTUAL
        if self._has_normative_language(sentence):
            return EpistemicIndicator.DEFERRED
        if self._has_interpretive_markers(sentence):
            return EpistemicIndicator.INTERPRETIVE
        return self._default_indicator
```

### 5.3.4 GNORM Integration (integrations/gnorm.py)

Integration with the GNORM CRF annotation service:

```python
class GNORMClient:
    """Client for GNORM named entity recognition service."""

    async def annotate(self, text: str) -> list[GNORMAnnotation]:
        """Submit text for CRF-based entity annotation."""

    def map_confidence_to_indicator(self, confidence: float) -> EpistemicIndicator:
        """Map GNORM confidence scores to epistemic indicators."""
        if confidence >= 0.9:
            return EpistemicIndicator.FACTUAL
        elif confidence >= 0.7:
            return EpistemicIndicator.INTERPRETIVE
        else:
            return EpistemicIndicator.DEFERRED
```

## 5.4 Configuration System

The agent uses environment-based configuration with sensible defaults:

```python
class AgentConfig(BaseSettings):
    """Configuration with ITSERR_ prefix for environment variables."""

    # LLM Configuration
    llm_provider: LLMProvider = LLMProvider.ANTHROPIC
    llm_model: str = "claude-sonnet-4-20250514"

    # Memory Configuration
    memory_persist_path: Path = Path("./data/memory")
    memory_top_k: int = 5
    reflection_trigger_count: int = 10

    # Epistemic Configuration
    epistemic_default: str = "INTERPRETIVE"
    high_confidence_threshold: float = 0.85

    # Tool Configuration
    tool_confirmation_enabled: bool = True
    auto_execute_read_only: bool = True
```

## 5.5 GNORM/ITSERR Integration

The prototype integrates with the broader ITSERR digital humanities ecosystem:

### 5.5.1 GNORM Integration Points

| GNORM Feature | Integration | Epistemic Handling |
|---------------|-------------|-------------------|
| Named entity recognition | Entity annotations in responses | Confidence → indicator mapping |
| CRF confidence scores | Inform epistemic classification | High → FACTUAL, Medium → INTERPRETIVE |
| Religious domain entities | Domain-specific recognition | Specialized handling for theological terms |

### 5.5.2 Future T-ReS Integration

The architecture supports future integration with T-ReS text analysis:

- **Quantitative patterns** → `[FACTUAL]` indicators
- **Structural analysis** → `[INTERPRETIVE]` indicators
- **Significance claims** → `[DEFERRED]` indicators

## 5.6 Testing Strategy

The implementation includes comprehensive testing:

| Test Category | Focus | Count |
|---------------|-------|-------|
| Unit tests | Individual component behavior | ~35 |
| Integration tests | Component interaction | ~13 |
| Epistemic tests | Indicator classification accuracy | ~20 |
| Memory tests | Stream operations, retrieval | ~15 |

### Example Test: Epistemic Classification

```python
def test_citation_classified_as_factual():
    classifier = EpistemicClassifier(config)
    text = "Gadamer published Truth and Method in 1960."
    result = classifier.classify_and_tag(text)
    assert "[FACTUAL]" in result

def test_theological_claim_deferred():
    classifier = EpistemicClassifier(config)
    text = "This text teaches that God's love is unconditional."
    result = classifier.classify_and_tag(text)
    assert "[DEFERRED]" in result
```

## 5.7 Deployment Considerations

### Local-First Design

The prototype prioritizes local execution:
- **ChromaDB**: Local persistence, no cloud dependency
- **Embeddings**: Local sentence-transformers by default
- **LLM**: Configurable (Anthropic/OpenAI via API)

### Privacy Preservation

- Research content stored locally only
- No telemetry or usage tracking
- API keys managed via environment variables

## 5.8 Known Limitations

Honest engineering requires acknowledging limitations:

1. **Sentence segmentation**: Current regex-based splitting; NLTK/spaCy recommended for production
2. **Reflection summarization**: Pattern-based extraction; LLM-based summarization planned
3. **MCP schema**: Basic implementation; full Model Context Protocol compliance pending
4. **GNORM live testing**: Client ready but not tested against live API

---

## Notes for Revision

- [ ] Add performance benchmarks
- [ ] Include error handling examples
- [ ] Document API rate limiting strategy
- [ ] Add deployment instructions
- [ ] Include screenshots of CLI interaction

---

**Word Count Target:** 1000-1200 words
**Current Draft:** ~900 words (structured outline with code)

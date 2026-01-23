# Memory API Reference

API documentation for the narrative memory system.

## NarrativeMemorySystem

The main memory management class.

```python
from itserr_agent.memory.narrative import NarrativeMemorySystem
from itserr_agent.core.config import AgentConfig
```

### Constructor

```python
NarrativeMemorySystem(config: AgentConfig)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `AgentConfig` | Configuration with memory settings |

### Methods

#### retrieve_context

```python
async def retrieve_context(
    self,
    query: str,
    session_id: str | None = None,
    top_k: int | None = None,
) -> str | None
```

Retrieve relevant context from memory for the given query.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The current user query |
| `session_id` | `str \| None` | Optional session filter |
| `top_k` | `int \| None` | Number of items to retrieve |

**Returns:** Formatted context string, or None if no relevant context found

#### store_exchange

```python
async def store_exchange(
    self,
    user_input: str,
    agent_response: str,
    session_id: str | None = None,
) -> None
```

Store a conversation exchange in memory.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_input` | `str` | The user's query |
| `agent_response` | `str` | The agent's response |
| `session_id` | `str \| None` | Optional session identifier |

#### store_research_note

```python
async def store_research_note(
    self,
    content: str,
    source: str | None = None,
    session_id: str | None = None,
) -> None
```

Store a research note (source consulted, annotation created).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | The research note content |
| `source` | `str \| None` | Source reference |
| `session_id` | `str \| None` | Session identifier |

#### store_decision

```python
async def store_decision(
    self,
    decision: str,
    alternatives: list[str] | None = None,
    rationale: str | None = None,
    session_id: str | None = None,
) -> None
```

Store a decision made during research.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `decision` | `str` | The decision made |
| `alternatives` | `list[str] \| None` | Alternatives considered |
| `rationale` | `str \| None` | Reasoning for the decision |
| `session_id` | `str \| None` | Session identifier |

#### persist

```python
async def persist() -> None
```

Persist memory to disk (ChromaDB auto-persists, but this ensures flush).

#### get_session_summary

```python
async def get_session_summary(session_id: str) -> str | None
```

Get a summary of a research session.

**Returns:** Summary string or None if no items found

## Memory Streams

### StreamType

```python
from itserr_agent.memory.streams import StreamType

class StreamType(str, Enum):
    CONVERSATION = "conversation"
    RESEARCH = "research"
    DECISION = "decision"
```

### MemoryItem

```python
from itserr_agent.memory.streams import MemoryItem

@dataclass
class MemoryItem:
    content: str
    stream_type: StreamType
    timestamp: datetime
    session_id: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `age_hours` | `float` | Age of item in hours |

#### Methods

```python
def to_dict(self) -> dict[str, Any]
```

Convert to dictionary for storage.

```python
@classmethod
def from_dict(cls, data: dict[str, Any]) -> MemoryItem
```

Create from dictionary.

### BaseStream

Base class for memory streams.

```python
from itserr_agent.memory.streams import BaseStream

class BaseStream:
    stream_type: StreamType

    def add(
        self,
        content: str,
        session_id: str = "default",
        **metadata
    ) -> MemoryItem

    def get_recent(
        self,
        count: int = 10,
        session_id: str | None = None
    ) -> list[MemoryItem]

    @property
    def count(self) -> int
```

### ConversationStream

```python
from itserr_agent.memory.streams import ConversationStream

stream = ConversationStream()
item = stream.add_exchange(
    user_input="What is hermeneutics?",
    agent_response="[FACTUAL] Hermeneutics is...",
    session_id="study-session"
)
```

### ResearchStream

```python
from itserr_agent.memory.streams import ResearchStream

stream = ResearchStream()

# Add a source
item = stream.add_source(
    citation="Gadamer, Truth and Method (1960)",
    notes="Key concept of Wirkungsgeschichte on pp. 267-274",
    session_id="gadamer-study"
)

# Add an annotation
item = stream.add_annotation(
    text="Understanding is always historically effected",
    annotation="This is the core of Gadamer's hermeneutics",
    source="Truth and Method, p. 268"
)
```

### DecisionStream

```python
from itserr_agent.memory.streams import DecisionStream

stream = DecisionStream()

# Record a decision
item = stream.add_decision(
    decision="Focus on early Barth rather than Church Dogmatics",
    rationale="Earlier works show development of dialectical theology",
    alternatives=["Church Dogmatics period", "Ethical writings"]
)

# Record a path choice
item = stream.add_path_choice(
    chosen_path="Christocentric reading of Romans",
    rejected_paths=["Lutheran law-gospel schema", "New Perspective approach"],
    reason="Aligns better with Barth's own methodology"
)
```

## Usage Examples

### Direct Memory Access

```python
from itserr_agent.memory.narrative import NarrativeMemorySystem
from itserr_agent.core.config import AgentConfig

config = AgentConfig()
memory = NarrativeMemorySystem(config)

# Store a research note
await memory.store_research_note(
    content="Augustine discusses memory in Confessions Book X",
    source="Confessions",
    session_id="augustine-memory"
)

# Store a decision
await memory.store_decision(
    decision="Interpret Augustine's memory as proto-phenomenological",
    rationale="Aligns with Ricoeur's reading",
    alternatives=["Platonic interpretation", "Purely theological reading"],
    session_id="augustine-memory"
)

# Retrieve context
context = await memory.retrieve_context(
    query="What have I noted about Augustine and memory?",
    session_id="augustine-memory"
)
print(context)
```

### Working with Streams Directly

```python
from itserr_agent.memory.streams import (
    ConversationStream,
    ResearchStream,
    DecisionStream,
)

# Create streams
conv = ConversationStream()
research = ResearchStream()
decisions = DecisionStream()

# Add items
conv.add_exchange(
    user_input="Tell me about Aquinas",
    agent_response="[FACTUAL] Thomas Aquinas (1225-1274)..."
)

research.add_source(
    citation="ST I, q.2, a.3",
    notes="The five ways to prove God's existence"
)

decisions.add_decision(
    decision="Focus on the Fifth Way (teleological argument)",
    rationale="Most relevant to contemporary discussions"
)

# Get recent items
recent = conv.get_recent(count=5)
for item in recent:
    print(f"{item.timestamp}: {item.content[:50]}...")
```

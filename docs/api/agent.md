# Agent API Reference

API documentation for the core agent module.

## ITSERRAgent

The main agent class that orchestrates the reasoning loop.

```python
from itserr_agent.core.agent import ITSERRAgent
from itserr_agent.core.config import AgentConfig
```

### Constructor

```python
ITSERRAgent(config: AgentConfig | None = None)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `AgentConfig \| None` | Configuration object. If None, loads from environment. |

**Example:**

```python
# With default configuration (from environment)
agent = ITSERRAgent()

# With custom configuration
config = AgentConfig(
    llm_provider=LLMProvider.ANTHROPIC,
    llm_model="claude-3-sonnet-20240229"
)
agent = ITSERRAgent(config)
```

### Methods

#### process

```python
async def process(
    self,
    user_input: str,
    session_id: str | None = None
) -> AIMessage
```

Process user input and generate a response with epistemic indicators.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_input` | `str` | The user's query or request |
| `session_id` | `str \| None` | Optional session identifier for memory isolation |

**Returns:** `AIMessage` containing the tagged response

**Example:**

```python
response = await agent.process(
    "What does Gadamer say about hermeneutics?",
    session_id="hermeneutics-study"
)
print(response.content)
```

#### close

```python
async def close() -> None
```

Clean up resources and persist memory.

**Example:**

```python
await agent.close()
```

#### clear_conversation

```python
def clear_conversation() -> None
```

Clear the current conversation history (memory is preserved).

**Example:**

```python
agent.clear_conversation()
```

### Properties

#### conversation_history

```python
@property
def conversation_history(self) -> list[BaseMessage]
```

Get a copy of the current conversation history.

**Returns:** List of `BaseMessage` objects

## AgentConfig

Configuration class using Pydantic settings.

```python
from itserr_agent.core.config import AgentConfig, LLMProvider, EmbeddingProvider
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `llm_provider` | `LLMProvider` | `ANTHROPIC` | LLM provider |
| `llm_model` | `str` | `"claude-sonnet-4-20250514"` | Model identifier |
| `llm_temperature` | `float` | `0.7` | Response temperature |
| `openai_api_key` | `str \| None` | `None` | OpenAI API key |
| `anthropic_api_key` | `str \| None` | `None` | Anthropic API key |
| `embedding_provider` | `EmbeddingProvider` | `LOCAL` | Embedding provider |
| `embedding_model` | `str` | `"all-MiniLM-L6-v2"` | Embedding model |
| `memory_persist_path` | `Path` | `"./data/memory"` | ChromaDB path |
| `memory_collection_name` | `str` | `"itserr_memory"` | Collection name |
| `memory_top_k` | `int` | `5` | Items to retrieve |
| `reflection_trigger_count` | `int` | `10` | Exchanges before reflection |
| `epistemic_default` | `str` | `"INTERPRETIVE"` | Default indicator |
| `high_confidence_threshold` | `float` | `0.85` | FACTUAL threshold |
| `low_confidence_threshold` | `float` | `0.5` | Review flag threshold |
| `gnorm_api_url` | `str \| None` | `None` | GNORM API endpoint (falls back to `http://localhost:8000` when unset) |
| `gnorm_api_key` | `str \| None` | `None` | GNORM API key |
| `gnorm_timeout` | `int` | `30` | GNORM timeout (seconds) |

### Methods

#### validate_api_keys

```python
def validate_api_keys() -> None
```

Validate that required API keys are present.

**Raises:** `ValueError` if required keys are missing

### Enums

#### LLMProvider

```python
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
```

#### EmbeddingProvider

```python
class EmbeddingProvider(str, Enum):
    OPENAI = "openai"
    LOCAL = "local"
```

## Usage Examples

### Basic Usage

```python
import asyncio
from itserr_agent.core.agent import ITSERRAgent

async def main():
    agent = ITSERRAgent()

    response = await agent.process("Tell me about Augustine's Confessions")
    print(response.content)

    await agent.close()

asyncio.run(main())
```

### With Session Management

```python
async def research_session():
    agent = ITSERRAgent()

    # First query
    r1 = await agent.process(
        "I'm researching Luther's concept of vocation",
        session_id="luther-study"
    )

    # Follow-up (agent has context)
    r2 = await agent.process(
        "How does this relate to his doctrine of the priesthood of all believers?",
        session_id="luther-study"
    )

    # Clear conversation but keep memory
    agent.clear_conversation()

    # New conversation in same session
    r3 = await agent.process(
        "What were we discussing about Luther?",
        session_id="luther-study"
    )
    # Agent retrieves relevant memory context

    await agent.close()
```

### Custom Configuration

```python
from itserr_agent.core.config import AgentConfig, LLMProvider, EmbeddingProvider

config = AgentConfig(
    llm_provider=LLMProvider.ANTHROPIC,
    llm_model="claude-3-opus-20240229",
    llm_temperature=0.5,
    embedding_provider=EmbeddingProvider.LOCAL,
    embedding_model="all-mpnet-base-v2",
    memory_top_k=10,
    high_confidence_threshold=0.9,
)

agent = ITSERRAgent(config)
```

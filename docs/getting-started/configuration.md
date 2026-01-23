# Configuration

The ITSERR Agent is configured via environment variables or a `.env` file.

## Configuration File

Create a `.env` file in the `03_prototype` directory:

```bash
# 03_prototype/.env

# === LLM Provider Settings ===
ITSERR_LLM_PROVIDER=anthropic  # openai or anthropic (default: anthropic)
ITSERR_LLM_MODEL=claude-sonnet-4-20250514
ITSERR_LLM_TEMPERATURE=0.7

# === API Keys ===
ITSERR_OPENAI_API_KEY=sk-...
ITSERR_ANTHROPIC_API_KEY=sk-ant-...

# === Embedding Settings ===
ITSERR_EMBEDDING_PROVIDER=local  # openai or local (default: local)
ITSERR_EMBEDDING_MODEL=all-MiniLM-L6-v2

# === Memory Settings ===
ITSERR_MEMORY_PERSIST_PATH=./data/memory
ITSERR_MEMORY_COLLECTION_NAME=itserr_memory
ITSERR_MEMORY_TOP_K=5
ITSERR_REFLECTION_TRIGGER_COUNT=10

# === Epistemic Classification ===
ITSERR_EPISTEMIC_DEFAULT=INTERPRETIVE
ITSERR_HIGH_CONFIDENCE_THRESHOLD=0.85
ITSERR_LOW_CONFIDENCE_THRESHOLD=0.5

# === GNORM Integration (Optional) ===
ITSERR_GNORM_API_URL=http://localhost:8000
ITSERR_GNORM_API_KEY=
ITSERR_GNORM_TIMEOUT=30

# === Logging ===
ITSERR_LOG_LEVEL=INFO
ITSERR_LOG_STRUCTURED=true
```

## Configuration Options

### LLM Provider

| Variable | Description | Default |
|----------|-------------|---------|
| `ITSERR_LLM_PROVIDER` | LLM provider (`openai` or `anthropic`) | `anthropic` |
| `ITSERR_LLM_MODEL` | Model identifier | `claude-sonnet-4-20250514` |
| `ITSERR_LLM_TEMPERATURE` | Response creativity (0.0-2.0) | `0.7` |

**Recommended Models:**

=== "OpenAI"

    - `gpt-4-turbo-preview` - Best quality
    - `gpt-4` - Stable, reliable
    - `gpt-3.5-turbo` - Faster, cheaper

=== "Anthropic"

    - `claude-3-opus-20240229` - Highest capability
    - `claude-3-sonnet-20240229` - Balanced
    - `claude-3-haiku-20240307` - Fast and efficient

### Embedding Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `ITSERR_EMBEDDING_PROVIDER` | Embedding source (`openai` or `local`) | `local` |
| `ITSERR_EMBEDDING_MODEL` | Model for embeddings | `all-MiniLM-L6-v2` |

**Local Embedding Models (default):**

```bash
ITSERR_EMBEDDING_PROVIDER=local
ITSERR_EMBEDDING_MODEL=all-MiniLM-L6-v2  # Fast, good quality (default)
# or
ITSERR_EMBEDDING_MODEL=all-mpnet-base-v2  # Higher quality, slower
```

### Memory Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `ITSERR_MEMORY_PERSIST_PATH` | ChromaDB storage location | `./data/memory` |
| `ITSERR_MEMORY_COLLECTION_NAME` | Collection name | `itserr_memory` |
| `ITSERR_MEMORY_TOP_K` | Items to retrieve | `5` |
| `ITSERR_REFLECTION_TRIGGER_COUNT` | Exchanges before summarization | `10` |

### Epistemic Classification

| Variable | Description | Default |
|----------|-------------|---------|
| `ITSERR_EPISTEMIC_DEFAULT` | Default indicator for ambiguous content | `INTERPRETIVE` |
| `ITSERR_HIGH_CONFIDENCE_THRESHOLD` | Threshold for FACTUAL classification | `0.85` |
| `ITSERR_LOW_CONFIDENCE_THRESHOLD` | Threshold below which to flag for review | `0.5` |

### GNORM Integration

| Variable | Description | Default |
|----------|-------------|---------|
| `ITSERR_GNORM_API_URL` | GNORM API endpoint | `http://localhost:8000` (fallback when unset) |
| `ITSERR_GNORM_API_KEY` | API authentication key | (none) |
| `ITSERR_GNORM_TIMEOUT` | Request timeout in seconds | `30` |

## Programmatic Configuration

You can also configure the agent in code:

```python
from itserr_agent.core.config import AgentConfig, LLMProvider, EmbeddingProvider

config = AgentConfig(
    llm_provider=LLMProvider.ANTHROPIC,
    llm_model="claude-3-sonnet-20240229",
    llm_temperature=0.5,
    embedding_provider=EmbeddingProvider.LOCAL,
    memory_top_k=10,
    high_confidence_threshold=0.9,
)

agent = ITSERRAgent(config)
```

## Environment-Specific Configurations

### Development

```bash
ITSERR_LOG_LEVEL=DEBUG
ITSERR_LLM_MODEL=claude-3-5-haiku-20241022  # Faster for testing
```

### Production

```bash
ITSERR_LOG_LEVEL=INFO
ITSERR_LOG_STRUCTURED=true
ITSERR_LLM_MODEL=claude-sonnet-4-20250514
ITSERR_HIGH_CONFIDENCE_THRESHOLD=0.9
```

## Validation

The agent validates configuration on startup:

```python
config = AgentConfig()
config.validate_api_keys()  # Raises if keys missing for selected provider
```

!!! tip "Configuration Debugging"

    Set `LOG_LEVEL=DEBUG` to see configuration values at startup.

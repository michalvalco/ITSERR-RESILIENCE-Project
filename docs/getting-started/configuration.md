# Configuration

The ITSERR Agent is configured via environment variables or a `.env` file.

## Configuration File

Create a `.env` file in the `03_prototype` directory:

```bash
# 03_prototype/.env

# === LLM Provider Settings ===
LLM_PROVIDER=openai          # openai or anthropic
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7

# === API Keys ===
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# === Embedding Settings ===
EMBEDDING_PROVIDER=openai    # openai or local
EMBEDDING_MODEL=text-embedding-3-small

# === Memory Settings ===
MEMORY_PERSIST_PATH=./data/memory
MEMORY_COLLECTION_NAME=itserr_memory
MEMORY_TOP_K=5
REFLECTION_TRIGGER_COUNT=10

# === Epistemic Classification ===
EPISTEMIC_DEFAULT=interpretive
HIGH_CONFIDENCE_THRESHOLD=0.85
LOW_CONFIDENCE_THRESHOLD=0.5

# === GNORM Integration (Optional) ===
GNORM_API_URL=http://localhost:8000
GNORM_API_KEY=
GNORM_TIMEOUT=30.0

# === Logging ===
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Configuration Options

### LLM Provider

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (`openai` or `anthropic`) | `openai` |
| `LLM_MODEL` | Model identifier | `gpt-4-turbo-preview` |
| `LLM_TEMPERATURE` | Response creativity (0.0-1.0) | `0.7` |

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
| `EMBEDDING_PROVIDER` | Embedding source (`openai` or `local`) | `openai` |
| `EMBEDDING_MODEL` | Model for embeddings | `text-embedding-3-small` |

**Local Embedding Models:**

```bash
EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=all-MiniLM-L6-v2  # Fast, good quality
# or
EMBEDDING_MODEL=all-mpnet-base-v2  # Higher quality, slower
```

### Memory Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `MEMORY_PERSIST_PATH` | ChromaDB storage location | `./data/memory` |
| `MEMORY_COLLECTION_NAME` | Collection name | `itserr_memory` |
| `MEMORY_TOP_K` | Items to retrieve | `5` |
| `REFLECTION_TRIGGER_COUNT` | Exchanges before summarization | `10` |

### Epistemic Classification

| Variable | Description | Default |
|----------|-------------|---------|
| `EPISTEMIC_DEFAULT` | Default indicator for ambiguous content | `interpretive` |
| `HIGH_CONFIDENCE_THRESHOLD` | Threshold for FACTUAL classification | `0.85` |
| `LOW_CONFIDENCE_THRESHOLD` | Threshold below which to flag for review | `0.5` |

### GNORM Integration

| Variable | Description | Default |
|----------|-------------|---------|
| `GNORM_API_URL` | GNORM API endpoint | `http://localhost:8000` |
| `GNORM_API_KEY` | API authentication key | (none) |
| `GNORM_TIMEOUT` | Request timeout in seconds | `30.0` |

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
LOG_LEVEL=DEBUG
LLM_MODEL=gpt-3.5-turbo  # Cheaper for testing
```

### Production

```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
LLM_MODEL=gpt-4-turbo-preview
HIGH_CONFIDENCE_THRESHOLD=0.9
```

## Validation

The agent validates configuration on startup:

```python
config = AgentConfig()
config.validate_api_keys()  # Raises if keys missing for selected provider
```

!!! tip "Configuration Debugging"

    Set `LOG_LEVEL=DEBUG` to see configuration values at startup.

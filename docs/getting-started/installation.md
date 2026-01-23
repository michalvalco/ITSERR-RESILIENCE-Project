# Installation

This guide covers how to install and set up the ITSERR AI Agent for development or use.

## Requirements

- **Python 3.11+** (3.12 also supported)
- **pip** or **uv** package manager
- API key for OpenAI or Anthropic

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/michalvalco/ITSERR-RESILIENCE-Project.git
cd ITSERR-RESILIENCE-Project/03_prototype
```

### 2. Create a Virtual Environment

=== "venv"

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

=== "uv"

    ```bash
    uv venv
    source .venv/bin/activate
    ```

### 3. Install the Package

=== "Standard Install"

    ```bash
    pip install -e .
    ```

=== "With Development Tools"

    ```bash
    pip install -e ".[dev]"
    ```

The development install includes:

- Testing tools (pytest, pytest-asyncio, pytest-cov)
- Code quality (ruff, mypy)
- Documentation (mkdocs, mkdocs-material)

### 4. Configure Environment Variables

Create a `.env` file in the `03_prototype` directory:

```bash
# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7

# API Keys (set at least one)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Memory Settings
MEMORY_PERSIST_PATH=./data/memory
MEMORY_COLLECTION_NAME=itserr_memory

# Optional: GNORM Integration
GNORM_API_URL=http://localhost:8000
GNORM_API_KEY=your-gnorm-key
```

!!! warning "API Key Security"

    Never commit `.env` files to version control. The `.gitignore` is configured to exclude them.

## Verifying the Installation

Run a quick test to verify everything is working:

```bash
# Check the CLI is available
itserr-agent --help

# Run the test suite
pytest
```

## Optional: Local Embeddings

By default, the agent can use OpenAI embeddings. For local embeddings (no API calls for memory):

```bash
# Embeddings are included in dependencies
# Configure in .env:
EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

The first run will download the embedding model (~80MB).

## Troubleshooting

### ChromaDB Issues

If you encounter ChromaDB errors:

```bash
pip install --upgrade chromadb
```

### Missing Dependencies

```bash
pip install -e ".[dev]" --force-reinstall
```

### API Key Errors

Ensure your API key is valid and has sufficient credits:

```bash
# Test OpenAI key
python -c "from openai import OpenAI; OpenAI().models.list()"
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Start using the agent
- [Configuration Reference](configuration.md) - All configuration options

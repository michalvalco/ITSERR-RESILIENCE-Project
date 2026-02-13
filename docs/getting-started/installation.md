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
# LLM Provider (default: anthropic)
# ITSERR_LLM_PROVIDER=anthropic
# ITSERR_LLM_MODEL=claude-sonnet-4-20250514

# API Keys - set the key for your chosen provider
# Default provider is Anthropic, so set this key:
ITSERR_ANTHROPIC_API_KEY=your-anthropic-key

# Or, to use OpenAI instead:
# ITSERR_LLM_PROVIDER=openai
# ITSERR_OPENAI_API_KEY=your-openai-key

# Memory Settings (defaults shown)
# ITSERR_MEMORY_PERSIST_PATH=./data/memory
# ITSERR_MEMORY_COLLECTION_NAME=itserr_memory

# Optional: GNORM Integration
# ITSERR_GNORM_API_URL=http://localhost:8000
# ITSERR_GNORM_API_KEY=your-gnorm-key
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

## Embeddings

By default, the agent uses **local embeddings** via SentenceTransformers (no API calls required for memory operations). The first run will download the embedding model (~80MB).

```bash
# Default configuration (local embeddings):
# ITSERR_EMBEDDING_PROVIDER=local
# ITSERR_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

To use OpenAI embeddings instead:

```bash
ITSERR_EMBEDDING_PROVIDER=openai
ITSERR_EMBEDDING_MODEL=text-embedding-3-small
ITSERR_OPENAI_API_KEY=your-openai-key
```

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

## OCR Pipeline Dependencies (Optional)

If you plan to run the OCR pipeline on actual PDF scans (e.g., for the Stöckel corpus), you need additional system applications and Python packages. These are **not required** for the AI agent itself or for running tests.

```bash
# Python packages (from 03_prototype/ directory)
pip install pytesseract pdf2image Pillow lxml
```

You also need **Tesseract OCR** (with Latin language data) and **Poppler** installed as system applications. See the [OCR Pipeline installation guide](../pipeline/overview.md#dependencies) for detailed platform-specific instructions (Windows, macOS, Linux).

## Next Steps

- [Quick Start Guide](quickstart.md) - Start using the agent
- [Configuration Reference](configuration.md) - All configuration options
- [OCR Pipeline](../pipeline/overview.md) - Set up the OCR pipeline for PDF processing

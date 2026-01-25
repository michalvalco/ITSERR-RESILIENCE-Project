# ITSERR Agent: Local Development Environment Setup

**Purpose:** Step-by-step guide for setting up the ITSERR Agent prototype development environment on Windows.

**Project Location:** `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype`

---

## Prerequisites

Before starting, ensure you have:
- [ ] Python 3.11 or higher installed (`python --version`)
- [ ] Git installed and configured
- [ ] An Anthropic API key (or OpenAI if preferred)
- [ ] Visual Studio Code or preferred IDE

---

## Step 1: Navigate to Project Directory

```powershell
cd C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype
```

---

## Step 2: Create Python Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Or for Command Prompt:
# .\.venv\Scripts\activate.bat
```

**Verify activation:** Your prompt should show `(.venv)` prefix.

---

## Step 3: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install package in development mode with all dependencies
pip install -e ".[dev]"
```

This installs:
- **Core:** langchain, langgraph, langchain-anthropic, langchain-openai, chromadb, sentence-transformers, mcp
- **Dev:** pytest, pytest-asyncio, ruff, mypy

---

## Step 4: Configure Environment Variables

```powershell
# Copy example to create your .env file
copy .env.example .env
```

**Edit `.env` file** with your actual values:

```ini
# Required: Set your Anthropic API key
ITSERR_ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Optional: Adjust model if needed
ITSERR_LLM_MODEL=claude-sonnet-4-20250514

# Local embeddings (no API key needed)
ITSERR_EMBEDDING_PROVIDER=local
ITSERR_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**Important:** Never commit your `.env` file to git (it's in `.gitignore`).

---

## Step 5: Verify Installation

```powershell
# Run the test suite
pytest tests/ -v

# Check linting
ruff check src/

# Check types (optional, may have some warnings)
mypy src/itserr_agent/
```

Expected: All core tests should pass. You may see warnings about GNORM integration (placeholder until Feb briefing).

---

## Step 6: First Run Test

```powershell
# Quick interactive test
python -c "
from itserr_agent.core.config import AgentConfig
from itserr_agent.core.agent import ITSERRAgent

config = AgentConfig()
print(f'LLM Provider: {config.llm_provider}')
print(f'Model: {config.llm_model}')
print(f'Embedding Provider: {config.embedding_provider}')
print('Configuration loaded successfully!')
"
```

---

## Project Structure Overview

```
03_prototype/
├── .env                    # Your local config (create from .env.example)
├── .env.example            # Template
├── pyproject.toml          # Dependencies and project config
├── architecture/           # Design documents
│   ├── epistemic_indicators.md
│   ├── memory_architecture.md
│   ├── system_design.md
│   └── tool_patterns.md
├── src/itserr_agent/       # Source code
│   ├── core/               # Agent and config
│   ├── epistemic/          # Classification system
│   ├── integrations/       # GNORM client (placeholder)
│   ├── memory/             # Narrative memory system
│   └── tools/              # Tool infrastructure
└── tests/                  # Test suite
```

---

## Key Commands Reference

| Task | Command |
|------|---------|
| Activate venv | `.\.venv\Scripts\Activate.ps1` |
| Run tests | `pytest tests/ -v` |
| Run specific test | `pytest tests/test_integration.py -v` |
| Lint code | `ruff check src/` |
| Format code | `ruff format src/` |
| Type check | `mypy src/itserr_agent/` |
| CLI (when ready) | `itserr-agent` |

---

## Troubleshooting

### "sentence-transformers" slow on first run
First time loading `all-MiniLM-L6-v2` downloads ~90MB model. Subsequent runs use cache.

### ChromaDB permissions error
Ensure `./data/memory` directory exists and is writable:
```powershell
mkdir -p data\memory
```

### API key not found
Check that:
1. `.env` file exists (not `.env.example`)
2. Key is properly set without quotes around value
3. No trailing whitespace

### Tests fail on GNORM integration
Expected until Feb 11-12 technical briefing. GNORM tests use placeholder API configuration.

---

## Development Workflow

1. **Before coding:** Activate venv, pull latest changes
2. **While coding:** Run relevant tests frequently
3. **Before commit:** Run full test suite + linting
4. **Architecture reference:** Read `architecture/` docs for design decisions

---

## What's Working (as of Jan 25, 2026)

| Component | Status |
|-----------|--------|
| Core Agent | ✅ Functional |
| Narrative Memory | ✅ Functional (ChromaDB + sentence-transformers) |
| Epistemic Indicators | ✅ Functional (FACTUAL/INTERPRETIVE/DEFERRED) |
| Tool Infrastructure | ⚠️ Base classes only |
| GNORM Integration | ⚠️ Placeholder (awaiting API details) |
| MCP Protocol | ❌ Not started |

---

## Next Session Prompt

Copy this to start a development session:

```
I'm setting up the ITSERR Agent development environment. The project is at:
C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\03_prototype

I've completed the setup steps in DEV_ENVIRONMENT_SETUP_PROMPT.md. 

Current priority: [INSERT YOUR FOCUS]
- [ ] Run tests and verify everything works
- [ ] Review architecture documents
- [ ] Work on [specific component]
- [ ] Debug [specific issue]

Please help me [specific task].
```

---

*Document created: January 25, 2026*
*Fellowship starts: February 10, 2026 (16 days)*

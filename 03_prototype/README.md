# 03_prototype

AI agent prototype development for the ITSERR/RESILIENCE project.

## Structure

```
03_prototype/
├── architecture/      # Design documents
└── code_notes/        # Technical decisions log
```

## Core Innovations

### 1. Narrative Memory System
Contextual continuity across research sessions, preserving the hermeneutical journey.

- Stores conversation history with semantic indexing
- Retrieves relevant past context for new queries
- Maintains researcher's interpretive trajectory

### 2. Epistemic Modesty Indicators
Clear differentiation between response types:

| Indicator | Meaning | Example |
|-----------|---------|---------|
| `[FACTUAL]` | Verifiable information | Dates, citations, definitions |
| `[INTERPRETIVE]` | AI-assisted analysis | Pattern identification, connections |
| `[DEFERRED]` | Requires human judgment | Theological claims, value judgments |

### 3. Human-Centered Tool-Calling Patterns
Ensuring researcher maintains agency and control:

- Transparent tool invocation (user sees what's being called)
- Confirmation for significant actions
- Easy override/correction mechanisms

## Technical Stack

- **Python 3.11+**
- **LangChain / LangGraph** — Agent orchestration
- **Model Context Protocol (MCP)** — Tool integration
- **ChromaDB** — Vector database for semantic memory

## Architecture Documents (`architecture/`)

| Document | Purpose |
|----------|---------|
| `system_design.md` | Overall architecture overview |
| `memory_architecture.md` | Narrative memory system design |
| `epistemic_indicators.md` | Modesty indicator implementation |
| `tool_patterns.md` | Human-centered tool-calling design |

## Code Notes (`code_notes/`)

Technical decision log documenting:

- Design choices and rationale
- Philosophical annotations mapping principles to code
- Integration notes with ITSERR/GNORM tools
- Lessons learned and iterations

## Development Timeline

| Week | Development Goals |
|------|-------------------|
| Week 1 | Environment setup, review GNORM patterns |
| Week 2 | Implement narrative memory architecture |
| Week 3 | Complete prototype, document codebase |

## Related Resources

- [GNORM Annotation Code](https://github.com/aesuli/CIC_annotation)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
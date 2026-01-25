# Introduction for Non-Specialists: A Beginner's Guide

This guide explains what the ITSERR/RESILIENCE AI Agent project is, why it exists, and how to use it — all in plain language. No prior technical or theological expertise required.

---

## What Is This Project?

**In one sentence:** This is an AI-powered research assistant designed specifically to help scholars study religious texts responsibly.

Think of it as having a knowledgeable research partner who:

- Remembers your previous conversations and research decisions
- Clearly tells you when it's stating facts versus making interpretations
- Knows when to step back and let you — the human expert — make the final call on theological matters

Unlike generic AI chatbots (like ChatGPT or Claude used directly), this system is purpose-built for the unique challenges of religious studies research, where mishandling sensitive content or presenting AI interpretations as established facts could cause real harm.

---

## Why Does This Exist?

### The Problem

Religious studies researchers face a dilemma with AI tools:

1. **Generic AI assistants** are powerful but dangerous for theological work — they might confidently present interpretations as facts, or make theological judgments that should be left to human scholars
2. **Existing academic tools** often lack the contextual memory needed for sustained research projects
3. **No current solution** explicitly tracks the difference between "verified information" and "AI-generated analysis"

### The Solution

This project creates an AI agent with three key innovations:

| Innovation | What It Does | Why It Matters |
|------------|--------------|----------------|
| **Narrative Memory** | Remembers your research journey across sessions | You don't have to re-explain your project every time |
| **Epistemic Indicators** | Labels every response as FACTUAL, INTERPRETIVE, or DEFERRED | You always know what you can trust vs. what needs verification |
| **Human-Centered Tools** | Asks permission before taking significant actions | You stay in control of your research process |

---

## Who Is This For?

This tool is designed for:

- **Religious studies scholars** conducting hermeneutical research
- **Theologians** exploring textual interpretation
- **Digital humanities researchers** working with religious texts
- **Graduate students** learning responsible AI-assisted research methods
- **Research institutions** wanting ethical AI integration

You don't need to be a programmer to use the basic features — though some familiarity with command-line interfaces helps.

---

## The Repository Structure Explained

The project is organized into numbered folders, each with a specific purpose:

```
ITSERR-RESILIENCE-Project/
│
├── 01_research/          # Academic foundation
├── 02_writing/           # Written outputs
├── 03_prototype/         # The actual software (main code lives here)
├── 04_presentations/     # Slides and visual materials
├── 05_admin/             # Project management
└── docs/                 # This documentation
```

### 01_research/ — The Academic Foundation

Contains the scholarly groundwork:

- **sources/** — Summaries of key academic papers and books
- **literature_notes/** — Annotated bibliographies organized by topic
- **epistemic_modesty_framework.md** — The philosophical foundation for how the AI handles uncertainty

*Purpose:* This isn't random reading — it's the intellectual framework that shapes how the AI behaves.

### 02_writing/ — Written Outputs

Contains the project deliverables:

- **working_paper/** — The main research paper being produced
- **blog_post/** — A public-facing summary for the ITSERR website

*Purpose:* Academic outputs that explain and justify the approach.

### 03_prototype/ — The Software

This is where the actual AI agent code lives:

```
03_prototype/
├── src/itserr_agent/    # Main Python package
│   ├── core/            # Agent brain (orchestration, config)
│   ├── memory/          # How it remembers conversations
│   ├── epistemic/       # How it classifies its responses
│   ├── tools/           # Actions it can take
│   └── integrations/    # Connections to external services
├── tests/               # Automated tests
├── architecture/        # Design documents
└── pyproject.toml       # Project configuration
```

*Purpose:* This is the working prototype you can actually run.

### 04_presentations/ — Visual Materials

Presentation slides for:

- Consortium partners (ITSERR network)
- Academic conferences
- Workshop demonstrations

### 05_admin/ — Project Management

- Timeline and milestones
- Correspondence templates
- Administrative documents

### docs/ — Documentation

The documentation site (what you're reading now), including:

- Getting started guides
- API references
- Conceptual explanations
- Research context

---

## The Technologies Used (In Plain English)

### Core Technologies

| Technology | What It Does | Plain English |
|------------|--------------|---------------|
| **Python** | Programming language | The language the software is written in |
| **LangChain/LangGraph** | Agent framework | The "skeleton" that structures how the AI thinks and acts |
| **ChromaDB** | Vector database | A specialized memory system that finds related information |
| **Sentence Transformers** | Text embeddings | Converts text into numbers so the computer can find similar content |

### AI Providers

The agent can use different AI "brains":

- **Anthropic Claude** (default) — The AI model that generates responses
- **OpenAI GPT** — An alternative option

You need an API key from one of these providers to use the agent (more on this below).

### User Interface

- **Typer/Rich** — Makes the command-line interface pretty and easy to use
- **MkDocs** — Generates this documentation website

---

## How Does It Process Input?

Here's what happens when you ask the agent a question:

### Step-by-Step Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. YOU TYPE A QUESTION                                         │
│     "What does Augustine say about time?"                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. MEMORY RETRIEVAL                                            │
│     Agent searches its memory for relevant past conversations   │
│     → Finds: you discussed Confessions last week                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. CONTEXT BUILDING                                            │
│     Combines: your question + memory + conversation history     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. AI GENERATION                                               │
│     Claude/GPT generates a response based on all context        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. EPISTEMIC CLASSIFICATION                                    │
│     Each sentence is labeled:                                   │
│     → [FACTUAL] for verifiable claims                           │
│     → [INTERPRETIVE] for AI analysis                            │
│     → [DEFERRED] for theological judgments                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. MEMORY STORAGE                                              │
│     This exchange is saved for future reference                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. RESPONSE DELIVERED                                          │
│     You see the tagged response with clear indicators           │
└─────────────────────────────────────────────────────────────────┘
```

### The Three Memory Streams

The agent maintains three separate "notebooks":

| Stream | What It Stores | How Long | Example |
|--------|----------------|----------|---------|
| **Conversation** | Recent back-and-forth | Until summarized | "You asked about Gadamer yesterday" |
| **Research** | Sources and notes | Long-term | "Note: connection between Kierkegaard and Bonhoeffer" |
| **Decision** | Methodological choices | Permanent | "Decided to focus on Lutheran hermeneutics" |

This means you can return weeks later and the agent remembers your research context.

---

## What Kind of Input Does It Accept?

### Text Queries

The primary input is natural language questions and requests:

```
Good inputs:
✓ "What does Gadamer say about prejudice in hermeneutics?"
✓ "Compare Luther's and Calvin's views on Scripture"
✓ "Help me find connections between these three sources"
✓ "Can you note this methodological decision for later?"

The agent works best with:
✓ Research-oriented questions
✓ Requests for synthesis across sources
✓ Hermeneutical and interpretive questions
✓ Note-taking and memory requests
```

### Session Management

You can organize your research into named sessions:

```bash
# Start a new session for a specific research project
itserr-agent chat --session "augustine-time-study"

# Return to that session later (memory persists)
itserr-agent chat --session "augustine-time-study"
```

### Configuration (Environment Variables)

The agent is configured through environment variables:

```bash
# Required: API key for the AI provider
ITSERR_ANTHROPIC_API_KEY="your-api-key"

# Optional: Customize behavior
ITSERR_LLM_MODEL="claude-sonnet-4-20250514"
ITSERR_MEMORY_PERSIST_PATH="./my-research-memory"
ITSERR_EPISTEMIC_DEFAULT="INTERPRETIVE"
```

---

## The Three Core Innovations in Detail

### 1. Narrative Memory System

**Problem it solves:** Generic AI has no memory between conversations. Every time you start a new chat, you lose all context.

**How it works:**
- Every exchange is converted to a numerical "embedding" (a mathematical representation)
- These embeddings are stored in a vector database (ChromaDB)
- When you ask a new question, the system finds similar past exchanges
- Relevant context is automatically included in the AI's input

**Example benefit:**
```
Week 1: "I'm researching Bonhoeffer's Nachfolge"
Week 2: "How does this relate to Kierkegaard?"
        → Agent remembers you're studying discipleship and
          automatically connects to your Bonhoeffer research
```

### 2. Epistemic Modesty Indicators

**Problem it solves:** AI often presents uncertain information with false confidence. In religious studies, this is particularly dangerous.

**How it works:**
1. The AI is instructed to tag its own responses
2. A rule-based classifier reviews the response to detect and tag any unlabelled sentences
3. Final output includes clear labels on all content

**The three indicators:**

| Tag | Meaning | What You Should Do |
|-----|---------|-------------------|
| `[FACTUAL]` | Verifiable information (dates, citations, definitions) | Can use with reasonable confidence; verify for publication |
| `[INTERPRETIVE]` | AI-generated analysis (patterns, connections, synthesis) | Treat as a hypothesis; requires your scholarly evaluation |
| `[DEFERRED]` | Theological truth claims, value judgments | The AI explicitly defers to your human judgment |

**Example output:**
```
[FACTUAL] Rudolf Bultmann published "Theology of the New Testament"
in 1951-1955.

[INTERPRETIVE] His demythologization program appears to share
assumptions with Heidegger's existentialist philosophy.

[DEFERRED] Whether Bultmann's approach adequately preserves the
kerygmatic core of Christian proclamation requires theological
judgment that exceeds AI competence.
```

### 3. Human-Centered Tool Patterns

**Problem it solves:** AI agents that take actions autonomously can cause unintended consequences. Researchers need to stay in control.

**How it works:**

Tools are categorized by how much autonomy they have:

| Category | Confirmation Required? | Example |
|----------|----------------------|---------|
| **Read-Only** | No — safe to auto-execute | Searching memory, retrieving information |
| **Note-Taking** | Optional notification | Creating a research note |
| **Modification** | Yes — explicit approval | Editing files, modifying data |
| **External** | Yes + first-time gate | Calling external APIs (like GNORM) |

**Example interaction:**
```
You: Annotate this text with GNORM

Agent: I'd like to call the GNORM annotation service. This is an
external API that will process your text.

This is the first time using this tool in this session.
Proceed? [y/n]
```

---

## How to Get Started

### Prerequisites

1. **Python 3.11 or higher** installed on your computer
2. **An API key** from Anthropic (Claude) or OpenAI (GPT)
3. **Basic comfort with command line** (Terminal on Mac/Linux, Command Prompt on Windows)

### Installation Steps

```bash
# 1. Clone or download the repository
git clone https://github.com/michalvalco/ITSERR-RESILIENCE-Project.git
cd ITSERR-RESILIENCE-Project

# 2. Navigate to the prototype directory
cd 03_prototype

# 3. Install the package
pip install -e ".[dev]"

# 4. Set up your API key
export ITSERR_ANTHROPIC_API_KEY="your-api-key-here"

# 5. Run the agent
itserr-agent chat
```

### Your First Conversation

```bash
$ itserr-agent chat

ITSERR Agent v0.1.0
Type 'exit' or 'quit' to end the session.
---

You: Hello, I'm researching early church hermeneutics.

Agent: [FACTUAL] I can assist with research on early church
hermeneutical methods, including the Alexandrian allegorical
school and the Antiochene literal-historical approach.

[INTERPRETIVE] This represents a foundational tension in
Christian interpretation that continues to influence
contemporary biblical scholarship.

What aspect would you like to explore first?
```

### Demo Mode (No API Key Required)

To explore the features without an API key:

```bash
itserr-agent demo
```

This runs a simulated demonstration of all three core innovations.

---

## What Still Needs to Happen

The prototype is functional but several areas need completion for full production use:

### Immediate Priorities

| Task | Status | Description |
|------|--------|-------------|
| **GNORM Integration Testing** | Pending | Need to test with live GNORM API endpoint at UniPa |
| **API Key Setup** | User Required | You must provide your own Anthropic or OpenAI API key |
| **Memory Path Configuration** | Optional | Default works; customize for multi-project setups |

### For Production Deployment

| Area | What's Needed |
|------|---------------|
| **Authentication** | User authentication if deployed as web service |
| **Rate Limiting** | Protect against API cost overruns |
| **Backup System** | Automated backup of ChromaDB memory stores |
| **Monitoring** | Logging and alerting for production use |
| **UI Layer** | Web interface for non-CLI users (optional) |

### For Research Completion

| Deliverable | Status |
|-------------|--------|
| Working Paper | In progress (02_writing/working_paper/) |
| Final Presentation | Prepared (04_presentations/) |
| Blog Post | Draft stage (02_writing/blog_post/) |
| GNORM Integration Demo | Awaiting API access |

---

## Frequently Asked Questions

### Do I need programming knowledge?

**For basic use:** No. The CLI interface is straightforward.
**For customization:** Yes, Python knowledge helps for extending the agent.

### Is my research data private?

Yes. Memory is stored locally on your machine (in `./data/memory` by default). The only external communication is with the AI provider (Anthropic/OpenAI) for generating responses.

### Can I use this offline?

Partially. The memory system works offline, but generating new AI responses requires internet access to the AI provider's API.

### How much does it cost?

The software is free (MIT license). However, you pay for AI API usage:
- **Anthropic Claude:** Approximately $3-15 per million tokens
- **OpenAI GPT-4:** Approximately $10-30 per million tokens

A typical research session might use 10,000-50,000 tokens, costing $0.03-$1.50.

### What makes this different from just using ChatGPT?

1. **Persistent memory** across sessions (ChatGPT forgets everything)
2. **Epistemic indicators** that label uncertainty (ChatGPT presents everything confidently)
3. **Human-centered tools** that ask permission (ChatGPT acts autonomously)
4. **Research-focused design** for religious studies specifically

### Can I contribute to the project?

Yes! The code is open source under MIT license. See the GitHub repository for contribution guidelines.

---

## Glossary

| Term | Definition |
|------|------------|
| **API Key** | A secret code that authenticates you with an AI service provider |
| **ChromaDB** | A database that stores information as numerical vectors for semantic search |
| **CLI** | Command Line Interface — text-based interaction (vs. graphical UI) |
| **Embedding** | A numerical representation of text that captures meaning |
| **Epistemic** | Relating to knowledge and how we know what we know |
| **GNORM** | A named entity recognition tool for religious texts (developed by ITSERR WP3) |
| **Hermeneutics** | The theory and methodology of interpretation, especially of texts |
| **LangChain** | A framework for building applications with large language models |
| **LLM** | Large Language Model — the AI that generates responses (Claude, GPT, etc.) |
| **MCP** | Model Context Protocol — a standard for connecting AI tools |
| **Token** | A unit of text (roughly 4 characters or 0.75 words) used for billing |
| **Vector Database** | A database optimized for finding similar items based on meaning |

---

## Next Steps

1. **Try the demo:** `itserr-agent demo` (no API key needed)
2. **Read the quickstart:** [Getting Started](getting-started/quickstart.md)
3. **Explore concepts:** [Epistemic Indicators](concepts/epistemic-indicators.md)
4. **Understand the architecture:** [System Design](architecture/system-design.md)

---

## Getting Help

- **Documentation:** You're reading it
- **Issues:** [GitHub Issues](https://github.com/michalvalco/ITSERR-RESILIENCE-Project/issues)
- **Project Context:** [About ITSERR](about/context.md)

---

*This guide was created as part of the ITSERR Transnational Access Fellowship, February 2026.*

# Quick Start

Get up and running with the ITSERR AI Agent in minutes.

## Starting a Chat Session

After [installation](installation.md), start an interactive session:

```bash
itserr-agent chat
```

You'll see a prompt where you can enter queries:

```
ITSERR Agent v0.1.0
Type 'exit' or 'quit' to end the session.
---

You: What can you tell me about Gadamer's hermeneutics?

Agent: [FACTUAL] Hans-Georg Gadamer (1900-2002) was a German philosopher
who developed philosophical hermeneutics, most notably in his 1960 work
"Truth and Method" (Wahrheit und Methode).

[INTERPRETIVE] His approach emphasizes the historical situatedness of
understanding and the concept of "Wirkungsgeschichte" (effective history),
which suggests that our interpretations are always shaped by tradition.

[DEFERRED] Whether Gadamer's rejection of methodological objectivity is
compatible with theological claims to truth is a matter requiring careful
theological reflection.
```

Notice how responses are tagged with epistemic indicators!

## Understanding Epistemic Indicators

The agent classifies each part of its response:

| Indicator | What It Means | Your Action |
|-----------|---------------|-------------|
| `[FACTUAL]` | Verifiable information | Can cite directly |
| `[INTERPRETIVE]` | AI analysis | Verify and refine |
| `[DEFERRED]` | Needs human judgment | Engage theologically |

## Example Research Session

Here's a typical research workflow:

```
You: I'm researching the relationship between Kierkegaard and Bonhoeffer
on the concept of discipleship.

Agent: [FACTUAL] Dietrich Bonhoeffer's "Nachfolge" (The Cost of Discipleship)
was published in 1937. Søren Kierkegaard wrote extensively on Christian
existence, particularly in "Training in Christianity" (1850).

[INTERPRETIVE] Both thinkers critique "cheap grace" and nominal Christianity,
though Kierkegaard focuses on individual existence while Bonhoeffer
emphasizes community and concrete obedience.

[INTERPRETIVE] There appears to be a trajectory from Kierkegaard's
"leap of faith" to Bonhoeffer's "costly grace" that merits further
exploration in your research.

[DEFERRED] The theological adequacy of either approach to discipleship
for contemporary contexts requires normative theological judgment.

You: Can you note this connection for future reference?

Agent: [FACTUAL] I've stored this research note in your session memory.
The connection between Kierkegaard's individual existence and Bonhoeffer's
communal discipleship has been recorded for future retrieval.
```

## Memory and Context

The agent maintains three memory streams:

1. **Conversation** - Recent exchanges (for context)
2. **Research** - Notes and sources (long-term)
3. **Decisions** - Methodological choices (preserved)

Start a new session with a specific ID to maintain context:

```bash
itserr-agent chat --session "kierkegaard-bonhoeffer-study"
```

## CLI Commands

```bash
# Interactive chat
itserr-agent chat

# Chat with specific session
itserr-agent chat --session "my-research"

# Run interactive demo (no API key required)
itserr-agent demo

# Run demo with live API calls
itserr-agent demo --live

# Show current configuration
itserr-agent config

# Show version
itserr-agent version

# Get help
itserr-agent --help
```

## Interactive Demo

The `demo` command provides an interactive demonstration of all three core innovations without requiring an API key:

```bash
itserr-agent demo
```

This launches a guided tour with three predefined scenarios:

1. **Theological Research Session** - Explore epistemic indicators in action
2. **Hermeneutical Exploration** - See factual vs. interpretive classification
3. **Memory Continuity Demo** - Observe narrative memory across exchanges

You can also choose **Custom Session** for interactive freeform exploration.

Use `--live` to enable actual LLM calls (requires configured API key).

## Programmatic Usage

Use the agent in your Python code:

```python
import asyncio
from itserr_agent.core.agent import ITSERRAgent
from itserr_agent.core.config import AgentConfig

async def main():
    config = AgentConfig()
    agent = ITSERRAgent(config)

    response = await agent.process(
        "What does Augustine say about time in Confessions Book XI?",
        session_id="augustine-study"
    )

    print(response.content)
    await agent.close()

asyncio.run(main())
```

## Next Steps

- [Configuration](configuration.md) - Customize the agent
- [Epistemic Indicators](../concepts/epistemic-indicators.md) - Deep dive into the classification system
- [Narrative Memory](../concepts/narrative-memory.md) - How memory works

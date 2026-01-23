# Human-Centered Tool-Calling Patterns: Architecture Detail

**Status:** Implementation Guide
**References:** `system_design.md` Section 3.3
**Implementation:** `src/itserr_agent/tools/`

---

## Overview

The Human-Centered Tool-Calling system maintains researcher agency through transparent, confirmable tool invocations. Unlike typical AI agents that execute tools silently, our approach ensures the researcher always knows what actions the agent is taking and can intervene.

---

## Design Principles

### 1. Transparency Over Efficiency

**Principle:** The researcher should always understand what the agent is doing.

**Implementation:**
- Pre-execution disclosure of intent
- Visible tool call logs
- Clear explanation of results

**Example:**
```
Agent: I'm going to search GNORM for entity annotations in the passage
       you quoted. This will identify named entities (people, places,
       concepts) and their relationships.

       [Proceed? Y/n]
```

### 2. Graduated Confirmation

**Principle:** Confirmation burden should match the risk/impact of the action.

**Implementation:**
- Read-only tools: Auto-execute (low risk)
- Note-taking tools: Optional confirmation (medium risk)
- Modification tools: Required confirmation (high risk)
- External tools: First-time gate + confirmation (trust building)

### 3. Reversibility Awareness

**Principle:** Make it clear which actions can be undone.

**Implementation:**
- Indicate reversibility in confirmation prompts
- Provide undo mechanisms where possible
- Warn clearly about irreversible actions

### 4. Override Mechanism

**Principle:** The researcher can always cancel, modify, or redirect.

**Implementation:**
- Timeout on confirmation prompts
- Clear "cancel" option
- Ability to modify parameters before execution

---

## Tool Categories

### Category 1: Read-Only Tools

**Definition:** Tools that retrieve information without modifying state.

**Confirmation:** None required (auto-execute)

**Examples:**
| Tool | Description |
|------|-------------|
| `search_bibliography` | Search the reference database |
| `lookup_citation` | Retrieve full citation details |
| `search_notes` | Search researcher's existing notes |
| `retrieve_memory` | Query the narrative memory system |
| `gnorm_annotate` | Get GNORM entity annotations (read from API) |

**Rationale:** These tools only gather information. The researcher can review results without any state change.

**Disclosure (minimal):**
```
Agent: Searching your notes for "hermeneutical circle"...
       Found 3 relevant notes.
```

---

### Category 2: Note-Taking Tools

**Definition:** Tools that create new artifacts (notes, annotations) in the researcher's workspace.

**Confirmation:** Optional (configurable)

**Examples:**
| Tool | Description |
|------|-------------|
| `create_note` | Create a new research note |
| `add_annotation` | Add annotation to a passage |
| `save_citation` | Save a citation to bibliography |
| `tag_source` | Add tags to a source |

**Rationale:** These create new content but don't modify existing work. Low risk, but researcher may want awareness.

**Disclosure:**
```
Agent: I'd like to create a note summarizing our discussion of Gadamer's
       horizon concept.

       Title: "Gadamer on Horizon Fusion"
       Tags: gadamer, hermeneutics, horizon

       [Create note? Y/n/edit]
```

**Configuration:**
```python
# In config
auto_confirm_note_taking: bool = True  # Skip confirmation if True
```

---

### Category 3: Modification Tools

**Definition:** Tools that modify existing files, notes, or research artifacts.

**Confirmation:** Always required

**Examples:**
| Tool | Description |
|------|-------------|
| `edit_note` | Modify an existing note |
| `update_citation` | Update citation metadata |
| `reorganize_tags` | Restructure tag hierarchy |
| `merge_notes` | Combine multiple notes |
| `delete_note` | Remove a note |

**Rationale:** Modifications to existing work can be disruptive. Researcher must explicitly approve.

**Disclosure (detailed):**
```
Agent: I'd like to update your note "Ricoeur Chapter Outline" to add
       a new section on distanciation.

       Changes:
       + Section 3.4: "Distanciation and Critical Distance"
       + Added reference: Ricoeur, "The Hermeneutical Function of
         Distanciation" (1973)

       This will modify your existing work.
       [Apply changes? Y/n/preview]
```

---

### Category 4: External Tools

**Definition:** Tools that interact with external services (APIs, databases outside the local system).

**Confirmation:** First-time gate + confirmation for sensitive operations

**Examples:**
| Tool | Description |
|------|-------------|
| `gnorm_annotate` | Request GNORM entity annotations |
| `tres_analyze` | Submit text to T-ReS for analysis |
| `fetch_doi` | Retrieve metadata from DOI registry |
| `search_jstor` | Search JSTOR database |

**First-Time Gate:**
```
Agent: This is the first time I'll be using the GNORM annotation service
       in this session. GNORM is part of the ITSERR project and will
       analyze your text for named entities.

       The text you shared will be sent to the GNORM API.

       [Enable GNORM for this session? Y/n/learn more]
```

After first-time approval, subsequent calls require only standard confirmation:
```
Agent: Sending this passage to GNORM for entity annotation...
       (GNORM access enabled earlier this session)
```

---

## Tool Interaction Flow

### Sequence Diagram

```
┌──────┐      ┌──────────┐      ┌────────────┐      ┌──────┐
│ User │      │  Agent   │      │ Tool Exec  │      │ Tool │
└──┬───┘      └────┬─────┘      └─────┬──────┘      └──┬───┘
   │   Query       │                  │                │
   │──────────────>│                  │                │
   │               │                  │                │
   │               │ Determine tools  │                │
   │               │ needed           │                │
   │               │                  │                │
   │               │ Check category   │                │
   │               │─────────────────>│                │
   │               │                  │                │
   │               │                  │ Read-only?     │
   │               │                  │────────────────│
   │               │                  │    Auto-exec   │
   │               │                  │<───────────────│
   │               │                  │                │
   │               │                  │ Needs confirm? │
   │               │<─────────────────│                │
   │               │                  │                │
   │  Confirm?     │                  │                │
   │<──────────────│                  │                │
   │               │                  │                │
   │   Yes/No      │                  │                │
   │──────────────>│                  │                │
   │               │                  │                │
   │               │  Execute         │                │
   │               │─────────────────>│                │
   │               │                  │ Call tool      │
   │               │                  │───────────────>│
   │               │                  │                │
   │               │                  │ Result         │
   │               │                  │<───────────────│
   │               │                  │                │
   │               │ Result           │                │
   │               │<─────────────────│                │
   │               │                  │                │
   │   Response    │                  │                │
   │<──────────────│                  │                │
```

---

## Implementation Details

### Tool Base Class

```python
class BaseTool(ABC):
    name: str
    description: str
    category: ToolCategory

    @property
    def requires_confirmation(self) -> bool:
        return self.category in (ToolCategory.MODIFICATION, ToolCategory.EXTERNAL)

    @property
    def requires_first_time_gate(self) -> bool:
        return self.category == ToolCategory.EXTERNAL and not self._first_use_confirmed

    def get_intent(self, **kwargs) -> ToolIntent:
        """Generate human-readable intent description."""
        return ToolIntent(
            tool_name=self.name,
            description=self._describe_action(**kwargs),
            parameters=kwargs,
            category=self.category,
            reversible=self._is_reversible(**kwargs),
        )

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool operation."""
        pass
```

### Confirmation Handler

```python
class ConfirmationHandler:
    """Handles user confirmation for tool execution."""

    async def request_confirmation(
        self,
        intent: ToolIntent,
        timeout: float = 30.0,
    ) -> ConfirmationResult:
        """
        Request user confirmation for a tool action.

        Returns:
            ConfirmationResult with decision and any modifications
        """
        # Display intent to user
        self._display_intent(intent)

        # Wait for user response
        response = await self._get_user_response(timeout)

        if response.action == "yes":
            return ConfirmationResult(confirmed=True)
        elif response.action == "no":
            return ConfirmationResult(confirmed=False, reason=response.reason)
        elif response.action == "edit":
            return ConfirmationResult(confirmed=True, modifications=response.edits)
        else:
            return ConfirmationResult(confirmed=False, reason="timeout")

    def _display_intent(self, intent: ToolIntent) -> None:
        """Display the tool intent in user-friendly format."""
        print(f"\n{intent.to_disclosure()}")

        if intent.parameters:
            print("\nParameters:")
            for key, value in intent.parameters.items():
                print(f"  {key}: {value}")

        if not intent.reversible:
            print("\n⚠️  This action cannot be undone.")

        print(f"\n[Proceed? Y/n{'/edit' if intent.category != ToolCategory.EXTERNAL else ''}]")
```

### Tool Registry

```python
class ToolRegistry:
    """Central registry for available tools."""

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._first_time_gates: set[str] = set()  # Tools that have passed first-time gate

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    async def execute(
        self,
        tool_name: str,
        confirmed: bool = False,
        **kwargs
    ) -> ToolResult:
        tool = self._tools.get(tool_name)
        if not tool:
            raise ToolNotFoundError(tool_name)

        # Check first-time gate for external tools
        if tool.category == ToolCategory.EXTERNAL:
            if tool_name not in self._first_time_gates:
                if not confirmed:
                    raise FirstTimeGateRequired(tool_name)
                self._first_time_gates.add(tool_name)

        # Check confirmation requirement
        if tool.requires_confirmation and not confirmed:
            raise ConfirmationRequired(tool.get_intent(**kwargs))

        # Execute
        return await tool.execute(**kwargs)
```

---

## MCP Integration

### Model Context Protocol

Tools are exposed via MCP for LLM integration:

```python
def get_mcp_schema(tool: BaseTool) -> dict:
    """Generate MCP-compatible tool schema."""
    return {
        "name": tool.name,
        "description": tool.description,
        "parameters": tool.parameter_schema,
        "metadata": {
            "category": tool.category.value,
            "requires_confirmation": tool.requires_confirmation,
            "reversible": tool.is_reversible,
        }
    }
```

### LangChain Tool Wrapper

```python
from langchain.tools import BaseTool as LCBaseTool

class LangChainToolWrapper(LCBaseTool):
    """Wrap ITSERR tools for LangChain compatibility."""

    name: str
    description: str
    _itserr_tool: BaseTool
    _confirmation_handler: ConfirmationHandler

    def _run(self, **kwargs) -> str:
        # Check confirmation
        if self._itserr_tool.requires_confirmation:
            intent = self._itserr_tool.get_intent(**kwargs)
            result = self._confirmation_handler.request_confirmation(intent)
            if not result.confirmed:
                return f"Action cancelled: {result.reason}"

        # Execute
        result = self._itserr_tool.execute(**kwargs)
        return self._itserr_tool.format_result(result)
```

---

## Built-In Tools

### Search Bibliography

```python
class SearchBibliographyTool(BaseTool):
    name = "search_bibliography"
    description = "Search the research bibliography for sources"
    category = ToolCategory.READ_ONLY

    async def execute(self, query: str, limit: int = 10) -> ToolResult:
        # Search implementation
        results = await self._search(query, limit)
        return ToolResult(
            success=True,
            data={"sources": results, "count": len(results)},
            tool_name=self.name,
            category=self.category,
        )
```

### Create Note

```python
class CreateNoteTool(BaseTool):
    name = "create_note"
    description = "Create a new research note"
    category = ToolCategory.NOTE_TAKING

    async def execute(
        self,
        title: str,
        content: str,
        tags: list[str] | None = None,
    ) -> ToolResult:
        note = Note(title=title, content=content, tags=tags or [])
        note_id = await self._storage.save(note)

        return ToolResult(
            success=True,
            data={"note_id": note_id, "title": title},
            tool_name=self.name,
            category=self.category,
        )
```

### GNORM Annotate

```python
class GNORMAnnotateTool(BaseTool):
    name = "gnorm_annotate"
    description = "Annotate text with GNORM named entity recognition"
    category = ToolCategory.EXTERNAL

    async def execute(
        self,
        text: str,
        entity_types: list[str] | None = None,
    ) -> ToolResult:
        response = await self._client.annotate(text, entity_types)

        # Map annotations to include epistemic indicators
        annotated = [
            {
                "text": a.entity_text,
                "type": a.entity_type,
                "confidence": a.confidence,
                "epistemic_indicator": a.epistemic_indicator.value,
            }
            for a in response.annotations
        ]

        return ToolResult(
            success=True,
            data={"annotations": annotated},
            tool_name=self.name,
            category=self.category,
        )
```

---

## User Interface Integration

### CLI Output

```
┌─────────────────────────────────────────────────────────────┐
│ Tool: gnorm_annotate                                         │
│ Category: EXTERNAL                                           │
├─────────────────────────────────────────────────────────────┤
│ I'm going to analyze this passage for named entities using  │
│ the GNORM annotation service.                               │
│                                                             │
│ Text to analyze:                                            │
│ "Augustine of Hippo developed his doctrine of divine        │
│  illumination in response to skeptical challenges..."       │
│                                                             │
│ This will send the text to the GNORM API.                   │
├─────────────────────────────────────────────────────────────┤
│ [Y] Proceed  [N] Cancel  [?] Learn more about GNORM         │
└─────────────────────────────────────────────────────────────┘
```

### Result Display

```
┌─────────────────────────────────────────────────────────────┐
│ GNORM Annotation Results                                     │
├─────────────────────────────────────────────────────────────┤
│ Found 4 entities:                                           │
│                                                             │
│ [FACTUAL] "Augustine of Hippo" - Person (94% confidence)    │
│ [FACTUAL] "Hippo" - Place (91% confidence)                  │
│ [INTERPRETIVE] "divine illumination" - Concept (68%)        │
│    ⚠️  Lower confidence - verify this identification        │
│ [INTERPRETIVE] "skeptical challenges" - Concept (62%)       │
│    ⚠️  Lower confidence - verify this identification        │
│                                                             │
│ Execution time: 234ms                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Considerations

### Input Validation

```python
def validate_tool_input(tool: BaseTool, **kwargs) -> None:
    """Validate tool inputs before execution."""
    # Check required parameters
    for param in tool.required_params:
        if param not in kwargs:
            raise MissingParameterError(param)

    # Validate parameter types
    for param, value in kwargs.items():
        expected_type = tool.param_types.get(param)
        if expected_type and not isinstance(value, expected_type):
            raise InvalidParameterType(param, expected_type, type(value))

    # Check for injection patterns in text inputs
    for param, value in kwargs.items():
        if isinstance(value, str) and contains_injection_pattern(value):
            raise PotentialInjectionError(param)
```

### Rate Limiting

```python
class RateLimiter:
    """Rate limit external tool calls."""

    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._calls: list[datetime] = []

    def check(self) -> bool:
        """Check if a call is allowed."""
        now = datetime.now()
        self._calls = [
            t for t in self._calls
            if (now - t).total_seconds() < self.window_seconds
        ]
        return len(self._calls) < self.max_calls

    def record(self) -> None:
        """Record a call."""
        self._calls.append(datetime.now())
```

---

## Implementation Checklist

- [ ] Base tool class with category system
- [ ] Tool registry with first-time gate tracking
- [ ] Confirmation handler with timeout
- [ ] MCP schema generation
- [ ] LangChain tool wrapper
- [ ] Built-in tools: search_bibliography, create_note, gnorm_annotate
- [ ] CLI confirmation UI
- [ ] Result formatting with epistemic indicators
- [ ] Input validation
- [ ] Rate limiting for external tools

---

## Configuration Options

```python
class ToolConfig:
    # Confirmation behavior
    auto_confirm_read_only: bool = True
    auto_confirm_note_taking: bool = False
    confirmation_timeout: float = 30.0

    # First-time gates
    require_first_time_gate: bool = True
    persist_first_time_approvals: bool = True  # Across sessions

    # Rate limiting
    external_rate_limit: int = 10  # calls per minute

    # Logging
    log_tool_calls: bool = True
    log_confirmations: bool = True
```

---

## References

- `system_design.md` - Parent architecture document
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- ITSERR guidelines on researcher agency

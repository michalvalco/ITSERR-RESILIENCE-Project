"""
Base tool definitions and categories.

Implements the human-centered tool pattern with different confirmation
requirements based on tool category.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolCategory(str, Enum):
    """
    Tool categories with different confirmation requirements.

    Based on the principle of maintaining researcher agency through
    transparent, confirmable tool invocations.
    """

    READ_ONLY = "read_only"
    """Search, lookup, retrieve - No confirmation required"""

    NOTE_TAKING = "note_taking"
    """Create note, add annotation - Optional confirmation"""

    MODIFICATION = "modification"
    """Edit file, update citation - Explicit confirmation required"""

    EXTERNAL = "external"
    """GNORM API, T-ReS query - Confirmation + first-time gate"""

    @property
    def requires_confirmation(self) -> bool:
        """Check if this category requires user confirmation."""
        return self in (ToolCategory.MODIFICATION, ToolCategory.EXTERNAL)

    @property
    def description(self) -> str:
        """Get a human-readable description of the category."""
        descriptions = {
            ToolCategory.READ_ONLY: "Read-only operations (auto-execute)",
            ToolCategory.NOTE_TAKING: "Note-taking operations (optional confirmation)",
            ToolCategory.MODIFICATION: "File modifications (confirmation required)",
            ToolCategory.EXTERNAL: "External API calls (confirmation + first-time gate)",
        }
        return descriptions[self]


@dataclass
class ToolResult:
    """
    Result of a tool execution.

    Includes both the result data and metadata for transparency.
    """

    success: bool
    data: Any
    tool_name: str
    category: ToolCategory
    execution_time_ms: float = 0.0
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def summary(self) -> str:
        """Get a brief summary of the result for logging."""
        if self.success:
            return f"{self.tool_name}: Success ({self.execution_time_ms:.0f}ms)"
        else:
            return f"{self.tool_name}: Failed - {self.error_message}"


@dataclass
class ToolIntent:
    """
    Represents the agent's intent to use a tool.

    Used for pre-execution disclosure: "I'm going to search GNORM for..."
    """

    tool_name: str
    description: str
    parameters: dict[str, Any]
    category: ToolCategory

    def to_disclosure(self) -> str:
        """Generate a human-readable disclosure of the intended action."""
        action_verbs = {
            ToolCategory.READ_ONLY: "search",
            ToolCategory.NOTE_TAKING: "create",
            ToolCategory.MODIFICATION: "modify",
            ToolCategory.EXTERNAL: "query",
        }
        verb = action_verbs.get(self.category, "use")
        return f"I'm going to {verb} {self.tool_name}: {self.description}"


class BaseTool(ABC):
    """
    Base class for all tools in the ITSERR agent.

    Tools implement the human-centered patterns:
    1. Pre-execution disclosure
    2. Confirmation for sensitive operations
    3. Transparent result presentation
    """

    name: str
    description: str
    category: ToolCategory

    def __init__(self) -> None:
        """Initialize the tool."""
        self._first_use_confirmed = False

    @property
    def requires_confirmation(self) -> bool:
        """Check if this tool requires user confirmation."""
        return self.category.requires_confirmation

    @property
    def requires_first_time_gate(self) -> bool:
        """Check if this tool requires first-time confirmation (external tools)."""
        return self.category == ToolCategory.EXTERNAL and not self._first_use_confirmed

    def confirm_first_use(self) -> None:
        """Mark first-time use as confirmed."""
        self._first_use_confirmed = True

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """
        Execute the tool operation.

        Subclasses must implement this method.

        Returns:
            ToolResult containing the operation outcome
        """
        pass

    def get_intent(self, **kwargs: Any) -> ToolIntent:
        """
        Get the intent description for this tool invocation.

        Used for pre-execution disclosure.
        """
        return ToolIntent(
            tool_name=self.name,
            description=self.description,
            parameters=kwargs,
            category=self.category,
        )

    def format_result(self, result: ToolResult) -> str:
        """
        Format the result for presentation to the user.

        Override in subclasses for custom formatting.
        """
        if not result.success:
            return f"Tool {self.name} failed: {result.error_message}"

        return f"Tool {self.name} completed successfully."

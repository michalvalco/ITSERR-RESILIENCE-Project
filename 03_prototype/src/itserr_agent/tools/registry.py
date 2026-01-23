"""
Tool Registry - Central management of available tools.

Handles tool registration, lookup, and MCP protocol integration.
"""

import time
from typing import Any

import structlog

from itserr_agent.tools.base import BaseTool, ToolCategory, ToolResult

logger = structlog.get_logger()


class ToolRegistry:
    """
    Central registry for all available tools.

    Manages tool lifecycle, lookup, and provides the interface
    for tool execution with human-centered patterns.
    """

    def __init__(self) -> None:
        """Initialize the registry."""
        self._tools: dict[str, BaseTool] = {}
        self._category_index: dict[ToolCategory, list[str]] = {
            category: [] for category in ToolCategory
        }

    def register(self, tool: BaseTool) -> None:
        """
        Register a tool with the registry.

        Args:
            tool: The tool instance to register

        Raises:
            ValueError: If a tool with the same name is already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")

        self._tools[tool.name] = tool
        self._category_index[tool.category].append(tool.name)

        logger.info(
            "tool_registered",
            tool_name=tool.name,
            category=tool.category.value,
        )

    def unregister(self, tool_name: str) -> None:
        """Remove a tool from the registry."""
        if tool_name not in self._tools:
            return

        tool = self._tools.pop(tool_name)
        self._category_index[tool.category].remove(tool_name)

        logger.info("tool_unregistered", tool_name=tool_name)

    def get(self, tool_name: str) -> BaseTool | None:
        """Get a tool by name."""
        return self._tools.get(tool_name)

    def get_by_category(self, category: ToolCategory) -> list[BaseTool]:
        """Get all tools in a category."""
        return [self._tools[name] for name in self._category_index[category]]

    def list_tools(self) -> list[dict[str, Any]]:
        """
        List all registered tools with their metadata.

        Returns a list suitable for display or LLM tool selection.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "category": tool.category.value,
                "requires_confirmation": tool.requires_confirmation,
            }
            for tool in self._tools.values()
        ]

    async def execute(
        self,
        tool_name: str,
        confirmed: bool = False,
        **kwargs: Any,
    ) -> ToolResult:
        """
        Execute a tool with human-centered patterns.

        Args:
            tool_name: Name of the tool to execute
            confirmed: Whether the user has confirmed the action
            **kwargs: Tool-specific parameters

        Returns:
            ToolResult from the tool execution

        Raises:
            ValueError: If tool not found or confirmation required but not given
        """
        tool = self.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")

        # Check confirmation requirements
        if tool.requires_confirmation and not confirmed:
            raise ValueError(
                f"Tool '{tool_name}' requires confirmation. "
                f"Category: {tool.category.description}"
            )

        # Check first-time gate for external tools
        if tool.requires_first_time_gate and not confirmed:
            raise ValueError(
                f"First-time use of external tool '{tool_name}' requires explicit confirmation"
            )

        if tool.category == ToolCategory.EXTERNAL and confirmed:
            tool.confirm_first_use()

        # Execute the tool
        start_time = time.perf_counter()

        try:
            result = await tool.execute(**kwargs)
            result.execution_time_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "tool_executed",
                tool_name=tool_name,
                success=result.success,
                execution_time_ms=result.execution_time_ms,
            )

            return result

        except Exception as e:
            logger.error(
                "tool_execution_failed",
                tool_name=tool_name,
                error=str(e),
            )

            return ToolResult(
                success=False,
                data=None,
                tool_name=tool_name,
                category=tool.category,
                error_message=str(e),
            )

    def get_mcp_definitions(self) -> list[dict[str, Any]]:
        """
        Get tool definitions in MCP (Model Context Protocol) format.

        Returns tool schemas suitable for LLM tool use.
        """
        # TODO: Implement proper MCP schema generation
        # For now, return simplified definitions
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": {},  # Would include JSON schema
            }
            for tool in self._tools.values()
        ]

    @property
    def tool_count(self) -> int:
        """Get the number of registered tools."""
        return len(self._tools)

    def __contains__(self, tool_name: str) -> bool:
        """Check if a tool is registered."""
        return tool_name in self._tools

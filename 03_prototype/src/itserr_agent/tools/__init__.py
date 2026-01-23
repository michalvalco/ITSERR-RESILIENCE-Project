"""
Tools module - Human-Centered Tool-Calling Patterns implementation.

This module implements the tool registry and tool definitions with
transparency and confirmation patterns:
- Read-only tools: Auto-execute
- Note-taking tools: Optional confirmation
- Modification tools: Explicit confirmation required
- External tools (GNORM, T-ReS): Confirmation + first-time gate
"""

from itserr_agent.tools.base import BaseTool, ToolCategory, ToolResult
from itserr_agent.tools.registry import ToolRegistry

__all__ = [
    "BaseTool",
    "ToolCategory",
    "ToolResult",
    "ToolRegistry",
]

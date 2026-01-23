"""
Core module - Agent orchestration and configuration.

This module contains the main agent implementation, configuration management,
and the core orchestration logic using LangGraph.
"""

from itserr_agent.core.agent import ITSERRAgent
from itserr_agent.core.config import AgentConfig

__all__ = [
    "ITSERRAgent",
    "AgentConfig",
]

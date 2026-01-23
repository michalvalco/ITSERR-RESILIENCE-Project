"""
ITSERR Agent - Ethically-grounded AI agent for religious studies research.

This package implements an AI research assistant prototype designed to support
theological and religious studies scholarship while maintaining epistemic
humility and human agency.

Core Innovations:
    1. Narrative Memory System - Preserves researcher's hermeneutical journey
    2. Epistemic Modesty Indicators - Differentiates facts from interpretations
    3. Human-Centered Tool Patterns - Maintains researcher control

Part of ITSERR WP5: AI-Assisted Resilience Development for Religious Studies.
"""

__version__ = "0.1.0"
__author__ = "ITSERR WP5 Team"

from itserr_agent.core.agent import ITSERRAgent
from itserr_agent.core.config import AgentConfig

__all__ = [
    "ITSERRAgent",
    "AgentConfig",
    "__version__",
]

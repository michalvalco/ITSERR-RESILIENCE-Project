"""
Memory module - Narrative Memory System implementation.

This module implements the three-stream memory architecture:
- Conversation Stream: Recent exchanges and clarifications
- Research Stream: Sources consulted and notes created
- Decision Stream: Choices made and alternatives considered

Uses ChromaDB for vector storage and semantic retrieval.
"""

from itserr_agent.memory.narrative import NarrativeMemorySystem
from itserr_agent.memory.streams import (
    ConversationStream,
    DecisionStream,
    MemoryItem,
    ResearchStream,
)

__all__ = [
    "NarrativeMemorySystem",
    "ConversationStream",
    "ResearchStream",
    "DecisionStream",
    "MemoryItem",
]

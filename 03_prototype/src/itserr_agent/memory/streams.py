"""
Memory stream definitions for the Narrative Memory System.

Each stream has distinct characteristics for retention and retrieval:
- Conversation: Recent exchanges, high recency weight
- Research: Sources and notes, high relevance weight
- Decision: Choices made, preserved long-term
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class StreamType(str, Enum):
    """Types of memory streams."""

    CONVERSATION = "conversation"
    RESEARCH = "research"
    DECISION = "decision"


@dataclass
class MemoryItem:
    """A single item in a memory stream.

    Note: All timestamps use UTC timezone for consistency across sessions
    and to avoid timezone-related issues in age calculations.
    """

    content: str
    stream_type: StreamType
    timestamp: datetime = field(default_factory=_utc_now)
    session_id: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def age_hours(self) -> float:
        """Calculate the age of this memory item in hours."""
        delta = datetime.now(timezone.utc) - self.timestamp
        return delta.total_seconds() / 3600

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "content": self.content,
            "stream_type": self.stream_type.value,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryItem":
        """Create from dictionary."""
        # Parse timestamp and normalize to UTC if naive (for backwards compatibility
        # with previously persisted data that may lack timezone info)
        timestamp = datetime.fromisoformat(data["timestamp"])
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        return cls(
            content=data["content"],
            stream_type=StreamType(data["stream_type"]),
            timestamp=timestamp,
            session_id=data.get("session_id", "default"),
            metadata=data.get("metadata", {}),
        )


class BaseStream:
    """Base class for memory streams."""

    stream_type: StreamType

    def __init__(self) -> None:
        self._items: list[MemoryItem] = []

    def add(self, content: str, session_id: str = "default", **metadata: Any) -> MemoryItem:
        """Add an item to the stream."""
        item = MemoryItem(
            content=content,
            stream_type=self.stream_type,
            session_id=session_id,
            metadata=metadata,
        )
        self._items.append(item)
        return item

    def get_recent(self, count: int = 10, session_id: str | None = None) -> list[MemoryItem]:
        """Get the most recent items from the stream."""
        items = self._items
        if session_id:
            items = [i for i in items if i.session_id == session_id]
        return sorted(items, key=lambda x: x.timestamp, reverse=True)[:count]

    @property
    def count(self) -> int:
        """Get the number of items in the stream."""
        return len(self._items)


class ConversationStream(BaseStream):
    """
    Conversation Stream - Recent exchanges and clarifications.

    Characteristics:
    - High recency weight in retrieval
    - Shorter retention (summarized after N exchanges)
    - Captures the flow of dialogue
    """

    stream_type = StreamType.CONVERSATION

    def add_exchange(
        self,
        user_input: str,
        agent_response: str,
        session_id: str = "default",
    ) -> MemoryItem:
        """Add a conversation exchange."""
        content = f"User: {user_input}\n\nAssistant: {agent_response}"
        return self.add(
            content=content,
            session_id=session_id,
            user_input=user_input,
            agent_response=agent_response,
        )


class ResearchStream(BaseStream):
    """
    Research Stream - Sources consulted and notes created.

    Characteristics:
    - High relevance weight in retrieval
    - Long retention (preserved across sessions)
    - Captures scholarly engagement
    """

    stream_type = StreamType.RESEARCH

    def add_source(
        self,
        citation: str,
        notes: str,
        session_id: str = "default",
    ) -> MemoryItem:
        """Add a consulted source with notes."""
        content = f"Source: {citation}\n\nNotes: {notes}"
        return self.add(
            content=content,
            session_id=session_id,
            citation=citation,
        )

    def add_annotation(
        self,
        text: str,
        annotation: str,
        source: str | None = None,
        session_id: str = "default",
    ) -> MemoryItem:
        """Add an annotation on a text."""
        content = f"Text: {text}\n\nAnnotation: {annotation}"
        if source:
            content += f"\n\nSource: {source}"
        return self.add(
            content=content,
            session_id=session_id,
            annotated_text=text,
            source=source,
        )


class DecisionStream(BaseStream):
    """
    Decision Stream - Choices made and alternatives considered.

    Characteristics:
    - Preserved long-term (important for research trajectory)
    - Captures reasoning and alternatives
    - Enables reflection on research direction
    """

    stream_type = StreamType.DECISION

    def add_decision(
        self,
        decision: str,
        rationale: str,
        alternatives: list[str] | None = None,
        session_id: str = "default",
    ) -> MemoryItem:
        """Add a research decision with rationale."""
        content = f"Decision: {decision}\n\nRationale: {rationale}"
        if alternatives:
            content += f"\n\nAlternatives considered: {', '.join(alternatives)}"
        return self.add(
            content=content,
            session_id=session_id,
            alternatives=alternatives or [],
        )

    def add_path_choice(
        self,
        chosen_path: str,
        rejected_paths: list[str],
        reason: str,
        session_id: str = "default",
    ) -> MemoryItem:
        """Record a methodological or interpretive path choice."""
        content = f"Chose: {chosen_path}\nRejected: {', '.join(rejected_paths)}\nReason: {reason}"
        return self.add(
            content=content,
            session_id=session_id,
            chosen_path=chosen_path,
            rejected_paths=rejected_paths,
        )

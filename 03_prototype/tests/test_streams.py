"""Tests for the memory streams module, focusing on timestamp handling."""

from datetime import datetime, timezone, timedelta

import pytest

from itserr_agent.memory.streams import (
    MemoryItem,
    StreamType,
    ConversationStream,
    ResearchStream,
    DecisionStream,
)


class TestMemoryItemTimestamps:
    """Tests for MemoryItem timestamp handling and UTC normalization."""

    def test_new_item_has_utc_timestamp(self) -> None:
        """New MemoryItems should have UTC timezone-aware timestamps."""
        item = MemoryItem(
            content="Test content",
            stream_type=StreamType.CONVERSATION,
        )
        assert item.timestamp.tzinfo is not None
        assert item.timestamp.tzinfo == timezone.utc

    def test_from_dict_naive_timestamp_treated_as_utc(self) -> None:
        """Naive timestamps (no timezone) should be treated as UTC."""
        data = {
            "content": "Test content",
            "stream_type": "conversation",
            "timestamp": "2025-01-15T10:30:00",  # Naive timestamp
            "session_id": "test",
            "metadata": {},
        }
        item = MemoryItem.from_dict(data)

        assert item.timestamp.tzinfo == timezone.utc
        assert item.timestamp.hour == 10
        assert item.timestamp.minute == 30

    def test_from_dict_utc_timestamp_preserved(self) -> None:
        """UTC timestamps should be preserved correctly."""
        data = {
            "content": "Test content",
            "stream_type": "conversation",
            "timestamp": "2025-01-15T10:30:00+00:00",  # UTC timestamp
            "session_id": "test",
            "metadata": {},
        }
        item = MemoryItem.from_dict(data)

        assert item.timestamp.tzinfo == timezone.utc
        assert item.timestamp.hour == 10
        assert item.timestamp.minute == 30

    def test_from_dict_non_utc_timestamp_normalized(self) -> None:
        """Non-UTC timestamps should be normalized to UTC."""
        # Timestamp in UTC+2 timezone
        data = {
            "content": "Test content",
            "stream_type": "conversation",
            "timestamp": "2025-01-15T12:30:00+02:00",  # UTC+2
            "session_id": "test",
            "metadata": {},
        }
        item = MemoryItem.from_dict(data)

        assert item.timestamp.tzinfo == timezone.utc
        # 12:30 UTC+2 = 10:30 UTC
        assert item.timestamp.hour == 10
        assert item.timestamp.minute == 30

    def test_from_dict_negative_offset_normalized(self) -> None:
        """Negative UTC offset timestamps should be normalized correctly."""
        # Timestamp in UTC-5 timezone
        data = {
            "content": "Test content",
            "stream_type": "conversation",
            "timestamp": "2025-01-15T05:30:00-05:00",  # UTC-5
            "session_id": "test",
            "metadata": {},
        }
        item = MemoryItem.from_dict(data)

        assert item.timestamp.tzinfo == timezone.utc
        # 05:30 UTC-5 = 10:30 UTC
        assert item.timestamp.hour == 10
        assert item.timestamp.minute == 30

    def test_to_dict_produces_iso_format(self) -> None:
        """to_dict should produce ISO format timestamp."""
        item = MemoryItem(
            content="Test content",
            stream_type=StreamType.CONVERSATION,
        )
        data = item.to_dict()

        assert "timestamp" in data
        # Should be parseable back
        parsed = datetime.fromisoformat(data["timestamp"])
        assert parsed.tzinfo is not None

    def test_roundtrip_preserves_timestamp(self) -> None:
        """Converting to dict and back should preserve timestamp."""
        original = MemoryItem(
            content="Test content",
            stream_type=StreamType.RESEARCH,
        )
        data = original.to_dict()
        restored = MemoryItem.from_dict(data)

        # Timestamps should be equal (within microseconds)
        diff = abs((original.timestamp - restored.timestamp).total_seconds())
        assert diff < 0.001

    def test_age_hours_calculation(self) -> None:
        """age_hours should calculate correctly using UTC."""
        # Create item with timestamp 2 hours ago
        two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
        item = MemoryItem(
            content="Test content",
            stream_type=StreamType.DECISION,
            timestamp=two_hours_ago,
        )

        # Should be approximately 2 hours
        assert 1.9 < item.age_hours < 2.1


class TestStreamTypes:
    """Tests for different stream types."""

    def test_conversation_stream_type(self) -> None:
        """ConversationStream should have correct stream type."""
        stream = ConversationStream()
        assert stream.stream_type == StreamType.CONVERSATION

    def test_research_stream_type(self) -> None:
        """ResearchStream should have correct stream type."""
        stream = ResearchStream()
        assert stream.stream_type == StreamType.RESEARCH

    def test_decision_stream_type(self) -> None:
        """DecisionStream should have correct stream type."""
        stream = DecisionStream()
        assert stream.stream_type == StreamType.DECISION


class TestConversationStream:
    """Tests for ConversationStream."""

    def test_add_exchange(self) -> None:
        """add_exchange should create properly formatted item."""
        stream = ConversationStream()
        item = stream.add_exchange(
            user_input="What is hermeneutics?",
            agent_response="Hermeneutics is the theory of interpretation.",
        )

        assert "User: What is hermeneutics?" in item.content
        assert "Assistant: Hermeneutics is the theory" in item.content
        assert item.stream_type == StreamType.CONVERSATION

    def test_get_recent_returns_newest_first(self) -> None:
        """get_recent should return items in reverse chronological order."""
        stream = ConversationStream()
        stream.add("First message")
        stream.add("Second message")
        stream.add("Third message")

        recent = stream.get_recent(2)
        assert len(recent) == 2
        assert "Third" in recent[0].content
        assert "Second" in recent[1].content


class TestResearchStream:
    """Tests for ResearchStream."""

    def test_add_source(self) -> None:
        """add_source should create properly formatted item."""
        stream = ResearchStream()
        item = stream.add_source(
            citation="Gadamer, H.-G. (1960). Truth and Method.",
            notes="Key work on philosophical hermeneutics.",
        )

        assert "Source: Gadamer" in item.content
        assert "Notes: Key work" in item.content
        assert item.stream_type == StreamType.RESEARCH

    def test_add_annotation(self) -> None:
        """add_annotation should create properly formatted item."""
        stream = ResearchStream()
        item = stream.add_annotation(
            text="The fusion of horizons",
            annotation="Central concept in Gadamer's hermeneutics",
            source="Truth and Method",
        )

        assert "Text: The fusion" in item.content
        assert "Annotation: Central concept" in item.content
        assert "Source: Truth and Method" in item.content


class TestDecisionStream:
    """Tests for DecisionStream."""

    def test_add_decision(self) -> None:
        """add_decision should create properly formatted item."""
        stream = DecisionStream()
        item = stream.add_decision(
            decision="Focus on Gadamer's hermeneutics",
            rationale="Most relevant to the research question",
            alternatives=["Ricoeur", "Heidegger"],
        )

        assert "Decision: Focus on Gadamer" in item.content
        assert "Rationale: Most relevant" in item.content
        assert "Alternatives considered: Ricoeur, Heidegger" in item.content
        assert item.stream_type == StreamType.DECISION

    def test_add_path_choice(self) -> None:
        """add_path_choice should record methodological choices."""
        stream = DecisionStream()
        item = stream.add_path_choice(
            chosen_path="Close reading approach",
            rejected_paths=["Distant reading", "Quantitative analysis"],
            reason="Better suited for theological texts",
        )

        assert "Chose: Close reading" in item.content
        assert "Rejected: Distant reading, Quantitative" in item.content
        assert "Reason: Better suited" in item.content

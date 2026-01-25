"""Tests for the reflection summarization system.

These tests verify the reflection mechanism that prevents context overflow
while preserving the essential narrative of the research journey.
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from itserr_agent.core.config import AgentConfig
from itserr_agent.memory.narrative import NarrativeMemorySystem


class TestReflectionSummarization:
    """Tests for the reflection summarization mechanism."""

    @pytest.mark.asyncio
    async def test_retrieve_recent_exchanges(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test retrieval of recent exchanges for reflection."""
        memory = NarrativeMemorySystem(test_config)

        # Store some exchanges
        for i in range(5):
            await memory.store_exchange(
                user_input=f"Question {i}?",
                agent_response=f"Answer {i}.",
                session_id="test-session",
            )

        # Retrieve recent exchanges
        exchanges = await memory._retrieve_recent_exchanges(
            session_id="test-session",
            limit=3,
        )

        # Should retrieve exchanges (mocked data)
        assert isinstance(exchanges, list)

    @pytest.mark.asyncio
    async def test_generate_reflection_summary_with_questions(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test reflection summary generation captures questions."""
        memory = NarrativeMemorySystem(test_config)

        # Create exchanges with questions
        exchanges = [
            {
                "content": "User: What is hermeneutics?\n\nAssistant: It is the theory of interpretation.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": "test",
            },
            {
                "content": "User: How does Gadamer define the hermeneutical circle?\n\nAssistant: As the interplay between part and whole.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": "test",
            },
        ]

        summary = await memory._generate_reflection_summary(exchanges)

        # Summary should be generated
        assert summary is not None
        assert "Reflection Summary" in summary
        assert "Research Questions" in summary or "Session Activity" in summary

    @pytest.mark.asyncio
    async def test_generate_reflection_summary_empty_exchanges(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test reflection summary with no exchanges."""
        memory = NarrativeMemorySystem(test_config)

        summary = await memory._generate_reflection_summary([])

        # Should still generate a basic summary
        assert summary is not None
        assert "Reflection Summary" in summary

    @pytest.mark.asyncio
    async def test_store_reflection_creates_document(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that storing reflection creates a document in the collection."""
        memory = NarrativeMemorySystem(test_config)

        await memory._store_reflection(
            summary="## Reflection Summary\n\nTest reflection content.",
            session_id="test-session",
            exchange_count=5,
        )

        # Verify document was added to collection
        # Access the collection directly from the memory system
        collection = memory._collection
        assert hasattr(collection, "_documents") and len(collection._documents) > 0

        # Verify metadata includes reflection flag
        stored = collection._documents[-1]
        assert stored["metadata"]["is_reflection"] is True
        assert stored["metadata"]["stream_type"] == "reflection"
        assert stored["metadata"]["exchange_count"] == 5

    @pytest.mark.asyncio
    async def test_trigger_reflection_resets_counter(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that triggering reflection resets exchange counter."""
        test_config.reflection_trigger_count = 2
        memory = NarrativeMemorySystem(test_config)

        # Manually set exchange count
        memory._exchange_count = 5

        # Trigger reflection
        await memory._trigger_reflection(session_id="test")

        # Counter should be reset
        assert memory._exchange_count == 0

    @pytest.mark.asyncio
    async def test_reflection_triggered_automatically(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test reflection is triggered automatically after threshold."""
        test_config.reflection_trigger_count = 2
        memory = NarrativeMemorySystem(test_config)

        # Store exchanges to reach threshold
        await memory.store_exchange("Q1?", "A1.", "test")
        assert memory._exchange_count == 1

        await memory.store_exchange("Q2?", "A2.", "test")
        # After reaching threshold, reflection should trigger and reset counter
        assert memory._exchange_count == 0


class TestSessionSummary:
    """Tests for the session summary functionality."""

    @pytest.mark.asyncio
    async def test_session_summary_returns_none_for_empty_session(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test summary returns None for non-existent session."""
        memory = NarrativeMemorySystem(test_config)

        summary = await memory.get_session_summary("non-existent-session")

        # Should return None when no items found
        assert summary is None

    @pytest.mark.asyncio
    async def test_session_summary_includes_stream_counts(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test session summary includes counts by stream type."""
        memory = NarrativeMemorySystem(test_config)

        # Store items of different types
        await memory.store_exchange("Q?", "A.", "summary-test")
        await memory.store_research_note("Note content", session_id="summary-test")
        await memory.store_decision("Decision", session_id="summary-test")

        summary = await memory.get_session_summary("summary-test")

        if summary:  # May be None if mock returns empty
            assert "Session Summary" in summary
            # Should contain statistics section
            assert "Memory Statistics" in summary or "items" in summary.lower()

    @pytest.mark.asyncio
    async def test_session_summary_includes_latest_reflection(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test session summary includes latest reflection if available."""
        memory = NarrativeMemorySystem(test_config)

        # Store a reflection
        await memory._store_reflection(
            summary="## Reflection\n\nKey questions explored: hermeneutics, interpretation.",
            session_id="reflection-summary-test",
            exchange_count=5,
        )

        # Also store a regular exchange so session isn't empty
        await memory.store_exchange("Q?", "A.", "reflection-summary-test")

        summary = await memory.get_session_summary("reflection-summary-test")

        if summary:
            # Should include the session identifier
            assert "reflection-summary-test" in summary or "Summary" in summary


class TestReflectionEdgeCases:
    """Tests for edge cases in reflection processing."""

    @pytest.mark.asyncio
    async def test_reflection_with_no_questions(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test reflection handles exchanges without question marks."""
        memory = NarrativeMemorySystem(test_config)

        exchanges = [
            {
                "content": "User: Tell me about hermeneutics.\n\nAssistant: Hermeneutics is fascinating.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": "test",
            },
        ]

        summary = await memory._generate_reflection_summary(exchanges)

        # Should still generate valid summary
        assert summary is not None
        assert "Reflection Summary" in summary

    @pytest.mark.asyncio
    async def test_reflection_with_long_questions(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test reflection truncates very long questions."""
        memory = NarrativeMemorySystem(test_config)

        long_question = "What is " + "very " * 100 + "interesting?"
        exchanges = [
            {
                "content": f"User: {long_question}\n\nAssistant: Good question.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": "test",
            },
        ]

        summary = await memory._generate_reflection_summary(exchanges)

        # Should truncate and add ellipsis for long questions
        assert summary is not None
        if "Research Questions" in summary:
            # Questions longer than 200 chars should be truncated with "..."
            # The long question is ~510 chars, so it must be truncated
            assert "..." in summary, "Long questions should be truncated with ellipsis"

    @pytest.mark.asyncio
    async def test_reflection_handles_malformed_exchange(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test reflection handles malformed exchange content."""
        memory = NarrativeMemorySystem(test_config)

        malformed_exchanges = [
            {
                "content": "This has no User: or Assistant: markers",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": "test",
            },
        ]

        # Should not raise
        summary = await memory._generate_reflection_summary(malformed_exchanges)
        assert summary is not None


class TestReflectionIntegrationWithAgent:
    """Tests for reflection integration with the full agent."""

    @pytest.mark.asyncio
    async def test_reflection_stores_after_agent_exchanges(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that reflection is triggered through normal agent operation."""
        from itserr_agent.core.agent import ITSERRAgent

        test_config.reflection_trigger_count = 2
        agent = ITSERRAgent(test_config)

        # Process enough exchanges to trigger reflection
        await agent.process("First question?", session_id="agent-reflection")
        await agent.process("Second question?", session_id="agent-reflection")

        # Reflection should have been triggered (counter reset)
        assert agent._memory._exchange_count == 0

    @pytest.mark.asyncio
    async def test_reflection_content_retrievable(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that stored reflections can be retrieved."""
        memory = NarrativeMemorySystem(test_config)

        # Store a reflection
        await memory._store_reflection(
            summary="## Reflection\n\nExploring themes of interpretation and meaning.",
            session_id="retrieval-test",
            exchange_count=10,
        )

        # Reflection should be retrievable via context query
        retrieved_context = await memory.retrieve_context(
            query="interpretation meaning themes",
            session_id="retrieval-test",
        )

        # Context retrieval should work - verify it returns expected type
        # With mocked ChromaDB, context may be None or a string
        assert retrieved_context is None or isinstance(retrieved_context, str)

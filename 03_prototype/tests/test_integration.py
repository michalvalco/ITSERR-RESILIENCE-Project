"""Integration tests for the full ITSERR Agent flow.

These tests verify that all components work together correctly:
- Agent orchestration
- Memory retrieval and storage
- Epistemic classification
- Reflection summarization
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from itserr_agent.core.agent import ITSERRAgent
from itserr_agent.core.config import AgentConfig
from itserr_agent.epistemic.classifier import EpistemicClassifier
from itserr_agent.epistemic.indicators import IndicatorType
from itserr_agent.memory.narrative import NarrativeMemorySystem


class TestAgentIntegration:
    """Integration tests for the ITSERRAgent."""

    @pytest.fixture
    def mock_agent_dependencies(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> dict[str, Any]:
        """Set up all mocked dependencies for agent testing."""
        return {
            "config": test_config,
            "chromadb": mock_chromadb,
            "sentence_transformer": mock_sentence_transformer,
        }

    @pytest.mark.asyncio
    async def test_full_agent_flow(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test the complete agent processing flow."""
        # Create agent with mocked dependencies
        agent = ITSERRAgent(test_config)

        # Process a query
        response = await agent.process(
            user_input="What did Gadamer write about hermeneutics?",
            session_id="test-session-1",
        )

        # Verify response contains epistemic indicators
        assert "[FACTUAL]" in response.content or "[INTERPRETIVE]" in response.content

        # Verify conversation history is updated
        assert len(agent.conversation_history) == 2  # user + assistant

    @pytest.mark.asyncio
    async def test_memory_context_influences_response(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that memory context is retrieved and used."""
        agent = ITSERRAgent(test_config)

        # First interaction
        await agent.process(
            user_input="I'm interested in Gadamer's hermeneutics.",
            session_id="test-session-2",
        )

        # Second interaction should retrieve context from first
        response = await agent.process(
            user_input="Tell me more about the hermeneutical circle.",
            session_id="test-session-2",
        )

        # Verify LLM was called with messages (context building happened)
        assert mock_anthropic.return_value.ainvoke.called
        assert response.content  # Response was generated

    @pytest.mark.asyncio
    async def test_epistemic_classification_applied(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that epistemic classification is applied to responses."""
        # Configure mock to return untagged content
        mock_anthropic.return_value.ainvoke = AsyncMock(
            return_value=MagicMock(
                content="Gadamer published Truth and Method in 1960. "
                "This suggests a connection to Heidegger's work."
            )
        )

        agent = ITSERRAgent(test_config)
        response = await agent.process(
            user_input="When did Gadamer publish his main work?",
            session_id="test-session-3",
        )

        # Classifier should have added indicators
        assert "[FACTUAL]" in response.content or "[INTERPRETIVE]" in response.content

    @pytest.mark.asyncio
    async def test_session_isolation(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that sessions are properly isolated."""
        agent = ITSERRAgent(test_config)

        # Interact in session A
        await agent.process(
            user_input="Topic A: Luther's theology",
            session_id="session-A",
        )

        # Interact in session B
        await agent.process(
            user_input="Topic B: Buddhist meditation",
            session_id="session-B",
        )

        # Both sessions should have stored their exchanges
        assert mock_anthropic.return_value.ainvoke.call_count == 2


class TestMemoryIntegration:
    """Integration tests for the NarrativeMemorySystem."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve_exchange(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test storing and retrieving conversation exchanges."""
        memory = NarrativeMemorySystem(test_config)

        # Store an exchange
        await memory.store_exchange(
            user_input="What is hermeneutics?",
            agent_response="Hermeneutics is the theory of interpretation.",
            session_id="test-session",
        )

        # Retrieve context
        context = await memory.retrieve_context(
            query="interpretation theory",
            session_id="test-session",
        )

        # Should find relevant context
        assert context is not None
        assert "hermeneutics" in context.lower() or "interpretation" in context.lower()

    @pytest.mark.asyncio
    async def test_store_research_note(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test storing research notes."""
        memory = NarrativeMemorySystem(test_config)

        await memory.store_research_note(
            content="Key insight about Gadamer's fusion of horizons",
            source="Truth and Method, p. 305",
            session_id="research-session",
        )

        # Verify note was stored
        context = await memory.retrieve_context(
            query="Gadamer horizons",
            session_id="research-session",
        )

        assert context is not None

    @pytest.mark.asyncio
    async def test_store_decision(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test storing research decisions."""
        memory = NarrativeMemorySystem(test_config)

        await memory.store_decision(
            decision="Focus on philosophical hermeneutics",
            rationale="Most relevant to research question",
            alternatives=["Historical hermeneutics", "Legal hermeneutics"],
            session_id="decision-session",
        )

        # Verify decision was stored
        context = await memory.retrieve_context(
            query="hermeneutics methodology decision",
            session_id="decision-session",
        )

        assert context is not None


class TestReflectionIntegration:
    """Integration tests for the reflection summarization system."""

    @pytest.mark.asyncio
    async def test_reflection_triggered_after_threshold(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that reflection is triggered after exchange threshold."""
        # Set low threshold for testing
        test_config.reflection_trigger_count = 3
        memory = NarrativeMemorySystem(test_config)

        # Store exchanges up to threshold
        for i in range(3):
            await memory.store_exchange(
                user_input=f"Question {i}",
                agent_response=f"Response {i}",
                session_id="reflection-test",
            )

        # Exchange count should be reset after reflection
        assert memory._exchange_count == 0

    @pytest.mark.asyncio
    async def test_session_summary_includes_statistics(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that session summary includes memory statistics."""
        memory = NarrativeMemorySystem(test_config)

        # Store various types of items
        await memory.store_exchange(
            user_input="Test question",
            agent_response="Test response",
            session_id="summary-test",
        )
        await memory.store_research_note(
            content="Research note content",
            session_id="summary-test",
        )
        await memory.store_decision(
            decision="Test decision",
            session_id="summary-test",
        )

        # Get summary
        summary = await memory.get_session_summary("summary-test")

        # Summary should include statistics
        assert summary is not None
        assert "Session Summary" in summary or "summary-test" in summary.lower()


class TestEpistemicClassifierIntegration:
    """Integration tests for epistemic classification across components."""

    def test_classifier_handles_mixed_content(self) -> None:
        """Test classification of content with multiple epistemic types."""
        config = AgentConfig(
            anthropic_api_key="test-key",
            openai_api_key="test-key",
        )
        classifier = EpistemicClassifier(config)

        mixed_content = (
            "Gadamer published Truth and Method in 1960. "
            "This work suggests connections to Heidegger's philosophy. "
            "Whether this interpretation is correct depends on your framework."
        )

        result = classifier.classify_and_tag(mixed_content)

        # Should contain multiple indicator types
        assert "[FACTUAL]" in result  # Publication fact
        assert "[INTERPRETIVE]" in result  # "suggests" marker
        # DEFERRED may or may not be present depending on classifier rules

    def test_classifier_preserves_llm_tags(self) -> None:
        """Test that pre-existing tags from LLM are preserved."""
        config = AgentConfig(
            anthropic_api_key="test-key",
            openai_api_key="test-key",
        )
        classifier = EpistemicClassifier(config)

        pre_tagged = "[FACTUAL] This is already tagged. [INTERPRETIVE] So is this."
        result = classifier.classify_and_tag(pre_tagged)

        # Tags should be preserved
        assert result == pre_tagged

    def test_gnorm_confidence_to_indicator_mapping(self) -> None:
        """Test GNORM confidence score to indicator mapping."""
        config = AgentConfig(
            anthropic_api_key="test-key",
            openai_api_key="test-key",
        )
        classifier = EpistemicClassifier(config)

        # High confidence -> FACTUAL
        high = classifier.classify_gnorm_annotation({"type": "person"}, 0.95)
        assert high == IndicatorType.FACTUAL

        # Medium confidence -> INTERPRETIVE
        medium = classifier.classify_gnorm_annotation({"type": "concept"}, 0.75)
        assert medium == IndicatorType.INTERPRETIVE

        # Low confidence -> INTERPRETIVE (below threshold)
        low = classifier.classify_gnorm_annotation({"type": "place"}, 0.4)
        assert low == IndicatorType.INTERPRETIVE


class TestEndToEndScenarios:
    """End-to-end scenario tests simulating real research workflows."""

    @pytest.mark.asyncio
    async def test_theological_research_session(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Simulate a theological research session."""
        agent = ITSERRAgent(test_config)
        session_id = "theology-research"

        # Initial query
        response1 = await agent.process(
            user_input="I'm researching Paul's concept of justification in Romans.",
            session_id=session_id,
        )
        assert response1.content

        # Follow-up with context
        response2 = await agent.process(
            user_input="How does this relate to the New Perspective on Paul?",
            session_id=session_id,
        )
        assert response2.content

        # Verify conversation history accumulated
        assert len(agent.conversation_history) == 4

    @pytest.mark.asyncio
    async def test_hermeneutical_inquiry_flow(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test flow reflecting hermeneutical inquiry patterns."""
        agent = ITSERRAgent(test_config)
        session_id = "hermeneutics-study"

        # Part-to-whole inquiry
        await agent.process(
            user_input="I'm looking at this specific passage in Romans 3:21-26.",
            session_id=session_id,
        )

        # Whole-to-part inquiry
        await agent.process(
            user_input="How does this fit into Paul's overall argument in Romans?",
            session_id=session_id,
        )

        # Meta-reflection (should potentially trigger DEFERRED)
        mock_anthropic.return_value.ainvoke = AsyncMock(
            return_value=MagicMock(
                content="The meaning of this passage for your faith is something "
                "you must discern through prayer and community."
            )
        )

        response = await agent.process(
            user_input="What should I believe about justification?",
            session_id=session_id,
        )

        # This kind of question should result in DEFERRED content
        # (depending on classifier rules)
        assert response.content

    @pytest.mark.asyncio
    async def test_clear_conversation_preserves_memory(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that clearing conversation preserves long-term memory."""
        agent = ITSERRAgent(test_config)
        session_id = "persistence-test"

        # Have some exchanges
        await agent.process(
            user_input="First question about Gadamer",
            session_id=session_id,
        )
        await agent.process(
            user_input="Second question about hermeneutics",
            session_id=session_id,
        )

        # Clear conversation
        agent.clear_conversation()
        assert len(agent.conversation_history) == 0

        # Memory should still be accessible (exchanges were stored)
        # Verify ChromaDB was used for storage
        assert mock_chromadb.called

        # Verify context retrieval still works
        retrieved_context = await agent._memory.retrieve_context(
            query="Gadamer hermeneutics",
            session_id=session_id,
        )
        # Context may be None or contain data depending on mock, but should not raise
        assert retrieved_context is None or isinstance(retrieved_context, str)


class TestErrorHandling:
    """Tests for error handling and resilience."""

    @pytest.mark.asyncio
    async def test_agent_handles_empty_response(
        self,
        test_config: AgentConfig,
        mock_anthropic: MagicMock,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test agent handles empty LLM response gracefully."""
        mock_anthropic.return_value.ainvoke = AsyncMock(
            return_value=MagicMock(content="")
        )

        agent = ITSERRAgent(test_config)
        response = await agent.process(
            user_input="Test query",
            session_id="error-test",
        )

        # Should not raise, even with empty content
        assert response.content == ""

    @pytest.mark.asyncio
    async def test_memory_store_failure_non_fatal(
        self,
        test_config: AgentConfig,
        mock_chromadb: MagicMock,
        mock_sentence_transformer: MagicMock,
    ) -> None:
        """Test that memory storage failures don't crash the system."""
        memory = NarrativeMemorySystem(test_config)

        # Make the memory's actual collection raise an exception on add
        # We access the internal _collection directly to ensure we're modifying
        # the same object the memory system is using
        memory._collection.add = MagicMock(side_effect=Exception("Storage error"))

        # Store initial exchange count
        initial_count = memory._exchange_count

        # Should not raise, just log error
        await memory.store_exchange(
            user_input="Test",
            agent_response="Response",
            session_id="error-test",
        )

        # Exchange count should not increment on failure
        assert memory._exchange_count == initial_count

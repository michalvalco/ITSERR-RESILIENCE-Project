"""
Main agent implementation using LangGraph.

This module contains the ITSERRAgent class, which orchestrates the agent's
reasoning loop, memory retrieval, tool execution, and response generation.
"""

from typing import Any

import structlog
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from itserr_agent.core.config import AgentConfig, LLMProvider
from itserr_agent.epistemic.classifier import EpistemicClassifier
from itserr_agent.memory.narrative import NarrativeMemorySystem

logger = structlog.get_logger()


class ITSERRAgent:
    """
    Ethically-grounded AI agent for religious studies research.

    This agent implements three core innovations:
    1. Narrative Memory System - Contextual continuity across sessions
    2. Epistemic Modesty Indicators - Clear differentiation of response types
    3. Human-Centered Tool Patterns - Transparent, confirmable tool use

    Example:
        ```python
        config = AgentConfig()
        agent = ITSERRAgent(config)

        response = await agent.process("What does Gadamer say about hermeneutics?")
        print(response.content)
        ```
    """

    def __init__(self, config: AgentConfig | None = None) -> None:
        """
        Initialize the ITSERR Agent.

        Args:
            config: Agent configuration. If None, loads from environment.
        """
        self.config = config or AgentConfig()
        self.config.validate_api_keys()

        self._llm = self._create_llm()
        self._memory = NarrativeMemorySystem(self.config)
        self._classifier = EpistemicClassifier(self.config)
        self._conversation_history: list[BaseMessage] = []

        logger.info(
            "agent_initialized",
            llm_provider=self.config.llm_provider.value,
            llm_model=self.config.llm_model,
        )

    def _create_llm(self) -> Any:
        """Create the LLM instance based on configuration."""
        if self.config.llm_provider == LLMProvider.OPENAI:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
                api_key=self.config.openai_api_key,
            )
        elif self.config.llm_provider == LLMProvider.ANTHROPIC:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
                api_key=self.config.anthropic_api_key,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.llm_provider}")

    async def process(self, user_input: str, session_id: str | None = None) -> AIMessage:
        """
        Process user input and generate a response.

        This is the main entry point for interacting with the agent. It:
        1. Retrieves relevant context from narrative memory
        2. Processes the input through the agent reasoning loop
        3. Classifies response content with epistemic indicators
        4. Updates memory with the exchange

        Args:
            user_input: The user's query or request
            session_id: Optional session identifier for memory isolation

        Returns:
            AIMessage containing the agent's response with epistemic indicators
        """
        logger.info("processing_input", input_length=len(user_input), session_id=session_id)

        # Step 1: Retrieve relevant memory context
        memory_context = await self._memory.retrieve_context(
            query=user_input,
            session_id=session_id,
        )

        # Step 2: Build messages with context
        messages = self._build_messages(user_input, memory_context)

        # Step 3: Generate response
        response = await self._llm.ainvoke(messages)

        # Step 4: Classify and tag with epistemic indicators
        # Note: We use a "belt-and-suspenders" approach here:
        # - The system prompt instructs the LLM to add epistemic indicators
        # - The classifier then validates/adds tags if the LLM missed any
        # The classifier preserves LLM-added tags (detected via regex) and only
        # adds classification to untagged sentences. This ensures consistent
        # indicator presence even when the LLM's instruction-following varies.
        tagged_response = self._classifier.classify_and_tag(response.content)

        # Step 5: Update memory
        await self._memory.store_exchange(
            user_input=user_input,
            agent_response=tagged_response,
            session_id=session_id,
        )

        # Step 6: Update conversation history
        self._conversation_history.append(HumanMessage(content=user_input))
        self._conversation_history.append(AIMessage(content=tagged_response))

        logger.info(
            "response_generated",
            response_length=len(tagged_response),
            session_id=session_id,
        )

        return AIMessage(content=tagged_response)

    def _build_messages(
        self,
        user_input: str,
        memory_context: str | None,
    ) -> list[BaseMessage]:
        """Build the message list for LLM invocation."""
        from langchain_core.messages import SystemMessage

        system_prompt = self._get_system_prompt(memory_context)

        messages: list[BaseMessage] = [SystemMessage(content=system_prompt)]
        messages.extend(self._conversation_history[-10:])  # Keep recent context
        messages.append(HumanMessage(content=user_input))

        return messages

    def _get_system_prompt(self, memory_context: str | None) -> str:
        """Generate the system prompt with memory context."""
        base_prompt = """You are an AI research assistant specialized in theological and religious studies.

You operate with three core principles:

1. EPISTEMIC MODESTY: Always classify your responses using these indicators:
   - [FACTUAL]: Verifiable information with citations (dates, quotes, bibliographic data)
   - [INTERPRETIVE]: AI-assisted analysis requiring researcher verification (patterns, connections)
   - [DEFERRED]: Matters requiring human judgment (theological truth claims, value judgments)

2. NARRATIVE CONTINUITY: You maintain awareness of the researcher's ongoing inquiry.
   Reference previous discussions when relevant and build upon established context.

3. TRANSPARENCY: Explain your reasoning. When uncertain, acknowledge it.
   When making connections, mark them as interpretive.

Format your responses with inline indicators, e.g.:
"[FACTUAL] Gadamer published Truth and Method in 1960. [INTERPRETIVE] This work appears
to connect with your earlier interest in hermeneutical approaches to biblical texts."
"""

        if memory_context:
            base_prompt += f"""

RELEVANT CONTEXT FROM PREVIOUS SESSIONS:
{memory_context}

Use this context to inform your response, but mark any references to it appropriately."""

        return base_prompt

    async def close(self) -> None:
        """Clean up resources and persist memory."""
        logger.info("closing_agent")
        await self._memory.persist()

    @property
    def conversation_history(self) -> list[BaseMessage]:
        """Get the current conversation history."""
        return self._conversation_history.copy()

    def clear_conversation(self) -> None:
        """Clear the current conversation history (memory is preserved)."""
        self._conversation_history.clear()
        logger.info("conversation_cleared")

    async def get_session_summary(self, session_id: str) -> str | None:
        """
        Get a summary of a research session.

        This provides a public interface to retrieve session summaries,
        including memory statistics and any reflection summaries generated
        during the session.

        Args:
            session_id: The session identifier to summarize

        Returns:
            A formatted summary string, or None if session not found
        """
        return await self._memory.get_session_summary(session_id)

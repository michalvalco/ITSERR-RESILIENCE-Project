"""
Narrative Memory System - Maintains contextual continuity across research sessions.

The narrative memory preserves the researcher's hermeneutical journey through
three distinct streams, each with different retention and retrieval characteristics.
"""

import uuid
from datetime import datetime, timezone
from typing import Any

import structlog

from itserr_agent.core.config import AgentConfig
from itserr_agent.memory.streams import ConversationStream, DecisionStream, ResearchStream

logger = structlog.get_logger()


class NarrativeMemorySystem:
    """
    Maintains contextual continuity across research sessions.

    Architecture:
    - Three memory streams (Conversation, Research, Decision)
    - Vector store (ChromaDB) for semantic retrieval
    - Reflection layer for periodic summarization

    Design Philosophy:
    Preserves the researcher's hermeneutical journey, not just data.
    Each interaction contributes to an evolving narrative of inquiry.
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the narrative memory system."""
        self.config = config
        self._client: Any = None
        self._collection: Any = None
        self._embeddings: Any = None

        # Memory streams
        self._conversation = ConversationStream()
        self._research = ResearchStream()
        self._decision = DecisionStream()

        # Track exchanges for reflection triggers
        self._exchange_count = 0

        self._initialize_storage()

    def _initialize_storage(self) -> None:
        """Initialize ChromaDB storage and embeddings."""
        import chromadb
        from chromadb.config import Settings

        # Initialize ChromaDB with persistence using PersistentClient (ChromaDB 0.4+)
        self._client = chromadb.PersistentClient(
            path=str(self.config.memory_persist_path),
            settings=Settings(
                anonymized_telemetry=False,
            ),
        )

        # Get or create collection
        self._collection = self._client.get_or_create_collection(
            name=self.config.memory_collection_name,
            metadata={"description": "ITSERR Agent narrative memory"},
        )

        # Initialize embeddings
        self._embeddings = self._create_embeddings()

        logger.info(
            "memory_initialized",
            persist_path=str(self.config.memory_persist_path),
            collection=self.config.memory_collection_name,
        )

    def _create_embeddings(self) -> Any:
        """Create the embedding function based on configuration."""
        from itserr_agent.core.config import EmbeddingProvider

        if self.config.embedding_provider == EmbeddingProvider.OPENAI:
            from langchain_openai import OpenAIEmbeddings

            return OpenAIEmbeddings(
                model=self.config.embedding_model,
                api_key=self.config.openai_api_key,
            )
        else:
            # Local embeddings using sentence-transformers
            from sentence_transformers import SentenceTransformer

            return SentenceTransformer(self.config.embedding_model)

    async def retrieve_context(
        self,
        query: str,
        session_id: str | None = None,
        top_k: int | None = None,
    ) -> str | None:
        """
        Retrieve relevant context from memory for the given query.

        Uses semantic similarity search with recency weighting to find
        the most relevant prior exchanges, research notes, and decisions.

        Args:
            query: The current user query
            session_id: Optional session filter
            top_k: Number of items to retrieve (defaults to config value)

        Returns:
            Formatted context string, or None if no relevant context found
        """
        k = top_k or self.config.memory_top_k

        # Generate embedding for query
        if hasattr(self._embeddings, "embed_query"):
            query_embedding = self._embeddings.embed_query(query)
        else:
            query_embedding = self._embeddings.encode(query).tolist()

        # Query ChromaDB
        where_filter = {"session_id": session_id} if session_id else None

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"] or not results["documents"][0]:
            return None

        # Format retrieved context
        context_parts = []
        for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            stream_type = meta.get("stream_type", "unknown")
            timestamp = meta.get("timestamp", "unknown")
            relevance = 1 - distance  # Convert distance to relevance

            context_parts.append(
                f"[{stream_type.upper()}] (relevance: {relevance:.2f}, from: {timestamp})\n{doc}"
            )

        logger.debug(
            "context_retrieved",
            num_items=len(context_parts),
            query_length=len(query),
        )

        return "\n\n---\n\n".join(context_parts)

    async def store_exchange(
        self,
        user_input: str,
        agent_response: str,
        session_id: str | None = None,
    ) -> None:
        """
        Store a conversation exchange in memory.

        This stores the exchange in the conversation stream and updates
        the vector store for future retrieval.

        Args:
            user_input: The user's query
            agent_response: The agent's response
            session_id: Optional session identifier
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Create document combining both sides of exchange
        doc = f"User: {user_input}\n\nAssistant: {agent_response}"

        # Generate embedding
        if hasattr(self._embeddings, "embed_query"):
            embedding = self._embeddings.embed_query(doc)
        else:
            embedding = self._embeddings.encode(doc).tolist()

        # Store in ChromaDB using UUID for unique document IDs
        doc_id = f"conv_{uuid.uuid4().hex}"

        try:
            self._collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[doc],
                metadatas=[
                    {
                        "stream_type": "conversation",
                        "timestamp": timestamp,
                        "session_id": session_id or "default",
                        "user_input_length": len(user_input),
                        "response_length": len(agent_response),
                    }
                ],
            )
        except Exception as exc:
            logger.error(
                "memory_store_failed",
                stream_type="conversation",
                doc_id=doc_id,
                error=str(exc),
            )
            # Continue without storing - memory is non-critical for agent operation
            return

        # Update exchange count and check for reflection trigger
        self._exchange_count += 1
        if self._exchange_count >= self.config.reflection_trigger_count:
            await self._trigger_reflection(session_id)

        logger.debug(
            "exchange_stored",
            doc_id=doc_id,
            session_id=session_id,
        )

    async def store_research_note(
        self,
        content: str,
        source: str | None = None,
        session_id: str | None = None,
    ) -> None:
        """Store a research note (source consulted, annotation created)."""
        timestamp = datetime.now(timezone.utc).isoformat()

        if hasattr(self._embeddings, "embed_query"):
            embedding = self._embeddings.embed_query(content)
        else:
            embedding = self._embeddings.encode(content).tolist()

        doc_id = f"research_{uuid.uuid4().hex}"

        try:
            self._collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[
                    {
                        "stream_type": "research",
                        "timestamp": timestamp,
                        "session_id": session_id or "default",
                        "source": source or "unknown",
                    }
                ],
            )
        except Exception as exc:
            logger.error(
                "memory_store_failed",
                stream_type="research",
                doc_id=doc_id,
                error=str(exc),
            )
            return

        logger.debug("research_note_stored", doc_id=doc_id)

    async def store_decision(
        self,
        decision: str,
        alternatives: list[str] | None = None,
        rationale: str | None = None,
        session_id: str | None = None,
    ) -> None:
        """Store a decision made during research."""
        timestamp = datetime.now(timezone.utc).isoformat()

        doc = f"Decision: {decision}"
        if rationale:
            doc += f"\nRationale: {rationale}"
        if alternatives:
            doc += f"\nAlternatives considered: {', '.join(alternatives)}"

        if hasattr(self._embeddings, "embed_query"):
            embedding = self._embeddings.embed_query(doc)
        else:
            embedding = self._embeddings.encode(doc).tolist()

        doc_id = f"decision_{uuid.uuid4().hex}"

        try:
            self._collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[doc],
                metadatas=[
                    {
                        "stream_type": "decision",
                        "timestamp": timestamp,
                        "session_id": session_id or "default",
                    }
                ],
            )
        except Exception as exc:
            logger.error(
                "memory_store_failed",
                stream_type="decision",
                doc_id=doc_id,
                error=str(exc),
            )
            return

        logger.debug("decision_stored", doc_id=doc_id)

    async def _trigger_reflection(self, session_id: str | None = None) -> None:
        """
        Trigger periodic reflection to summarize recent exchanges.

        This prevents context window overflow while preserving
        the essential narrative of the research journey.
        """
        logger.info(
            "reflection_triggered",
            exchange_count=self._exchange_count,
            session_id=session_id,
        )

        # TODO: Implement reflection summarization
        # 1. Retrieve recent exchanges
        # 2. Generate summary: "What questions has the researcher been exploring?"
        # 3. Store summary as a special reflection document
        # 4. Optionally archive/compress older detailed exchanges

        self._exchange_count = 0

    async def persist(self) -> None:
        """Persist memory to disk."""
        if self._client:
            # ChromaDB with persistence auto-saves, but we can force it
            logger.info("memory_persisted")

    async def get_session_summary(self, session_id: str) -> str | None:
        """Get a summary of a research session."""
        # Query for all items in session
        results = self._collection.query(
            query_texts=["session summary overview"],
            n_results=20,
            where={"session_id": session_id},
            include=["documents", "metadatas"],
        )

        if not results["documents"] or not results["documents"][0]:
            return None

        # TODO: Generate proper summary using LLM
        return f"Session {session_id}: {len(results['documents'][0])} memory items stored."

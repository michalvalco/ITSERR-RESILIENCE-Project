"""Shared test fixtures and configuration for ITSERR Agent tests."""

import os
import tempfile
from pathlib import Path
from typing import Any, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from itserr_agent.core.config import AgentConfig, EmbeddingProvider, LLMProvider


@pytest.fixture
def temp_memory_path() -> Generator[Path, None, None]:
    """Create a temporary directory for memory storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "memory"


@pytest.fixture
def test_config(temp_memory_path: Path) -> AgentConfig:
    """Create a test configuration with mocked API keys."""
    # Set environment variables for test
    os.environ["ITSERR_ANTHROPIC_API_KEY"] = "test-api-key"
    os.environ["ITSERR_OPENAI_API_KEY"] = "test-openai-key"

    return AgentConfig(
        llm_provider=LLMProvider.ANTHROPIC,
        llm_model="claude-sonnet-4-20250514",
        anthropic_api_key="test-api-key",
        openai_api_key="test-openai-key",
        embedding_provider=EmbeddingProvider.LOCAL,
        embedding_model="all-MiniLM-L6-v2",
        memory_persist_path=temp_memory_path,
        memory_collection_name="test_memory",
        memory_top_k=3,
        reflection_trigger_count=3,  # Low for testing
        high_confidence_threshold=0.85,
        low_confidence_threshold=0.5,
    )


@pytest.fixture
def mock_llm() -> MagicMock:
    """Create a mock LLM that returns predictable responses."""
    mock = MagicMock()
    mock.ainvoke = AsyncMock(
        return_value=MagicMock(
            content="[FACTUAL] Gadamer published Truth and Method in 1960. "
            "[INTERPRETIVE] This work connects to your interest in hermeneutics."
        )
    )
    return mock


@pytest.fixture
def mock_embeddings() -> MagicMock:
    """Create mock embeddings that return consistent vectors."""
    mock = MagicMock()
    # Return a simple embedding vector
    mock.encode.return_value = [0.1] * 384  # MiniLM dimension
    mock.embed_query.return_value = [0.1] * 384
    return mock


@pytest.fixture
def mock_anthropic() -> Generator[MagicMock, None, None]:
    """Mock the ChatAnthropic class.
    
    Note: We patch at the source library level because agent.py uses
    lazy imports inside the _create_llm() method.
    """
    with patch("langchain_anthropic.ChatAnthropic") as mock:
        mock_instance = MagicMock()
        mock_instance.ainvoke = AsyncMock(
            return_value=MagicMock(
                content="[FACTUAL] Test response with citations (Author, 2020). "
                "[INTERPRETIVE] This suggests an interesting pattern."
            )
        )
        mock.return_value = mock_instance
        yield mock


@pytest.fixture
def mock_sentence_transformer() -> Generator[MagicMock, None, None]:
    """Mock SentenceTransformer to avoid loading model in tests.
    
    Note: We patch at the source library level because narrative.py uses
    lazy imports inside the _create_embeddings() method.
    """
    with patch("sentence_transformers.SentenceTransformer") as mock:
        mock_instance = MagicMock()
        mock_instance.encode.return_value = [0.1] * 384
        mock.return_value = mock_instance
        yield mock


class MockChromaCollection:
    """Mock ChromaDB collection for testing."""

    def __init__(self) -> None:
        self._documents: list[dict[str, Any]] = []

    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """Store documents in mock collection."""
        for doc_id, embedding, doc, meta in zip(ids, embeddings, documents, metadatas):
            self._documents.append({
                "id": doc_id,
                "embedding": embedding,
                "document": doc,
                "metadata": meta,
            })

    def query(
        self,
        query_embeddings: list[list[float]] | None = None,
        query_texts: list[str] | None = None,
        n_results: int = 5,
        where: dict[str, Any] | None = None,
        include: list[str] | None = None,
    ) -> dict[str, Any]:
        """Query mock collection."""
        # Filter by where clause if provided
        filtered = self._documents
        if where:
            filtered = [
                d for d in filtered
                if all(d["metadata"].get(k) == v for k, v in where.items())
            ]

        # Return up to n_results
        results = filtered[:n_results]

        return {
            "ids": [[d["id"] for d in results]],
            "documents": [[d["document"] for d in results]],
            "metadatas": [[d["metadata"] for d in results]],
            "distances": [[0.1] * len(results)],
        }

    def count(self) -> int:
        """Return document count."""
        return len(self._documents)


@pytest.fixture
def mock_chromadb() -> Generator[MagicMock, None, None]:
    """Mock ChromaDB client and collection.
    
    Note: We patch at the source library level because narrative.py uses
    lazy imports inside the _initialize_storage() method.
    """
    with patch("chromadb.PersistentClient") as mock_persistent_client:
        mock_client = MagicMock()
        mock_collection = MockChromaCollection()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_persistent_client.return_value = mock_client
        yield mock_persistent_client

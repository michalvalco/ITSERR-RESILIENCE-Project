"""
Configuration management for the ITSERR Agent.

Handles environment variables, model selection, and feature flags.
"""

from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class EmbeddingProvider(str, Enum):
    """Supported embedding providers."""

    OPENAI = "openai"
    LOCAL = "local"  # sentence-transformers


class AgentConfig(BaseSettings):
    """
    Configuration for the ITSERR Agent.

    Configuration is loaded from environment variables with the ITSERR_ prefix.
    Example: ITSERR_LLM_PROVIDER=anthropic
    """

    model_config = SettingsConfigDict(
        env_prefix="ITSERR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Configuration
    llm_provider: LLMProvider = Field(
        default=LLMProvider.ANTHROPIC,
        description="LLM provider to use for agent responses",
    )
    llm_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Specific model identifier",
    )
    llm_temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for LLM responses",
    )

    # API Keys (loaded from environment)
    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key",
    )
    anthropic_api_key: str | None = Field(
        default=None,
        description="Anthropic API key",
    )

    # Embedding Configuration
    embedding_provider: EmbeddingProvider = Field(
        default=EmbeddingProvider.LOCAL,
        description="Embedding provider for vector storage",
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Embedding model identifier",
    )

    # Memory Configuration
    memory_persist_path: Path = Field(
        default=Path("./data/memory"),
        description="Path for persistent memory storage",
    )
    memory_collection_name: str = Field(
        default="itserr_memory",
        description="ChromaDB collection name",
    )
    memory_top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of memory items to retrieve",
    )
    reflection_trigger_count: int = Field(
        default=10,
        ge=1,
        description="Number of exchanges before triggering reflection",
    )

    # Epistemic Indicator Configuration
    epistemic_default: Literal["FACTUAL", "INTERPRETIVE", "DEFERRED"] = Field(
        default="INTERPRETIVE",
        description="Default indicator when classification is uncertain",
    )
    high_confidence_threshold: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for FACTUAL classification",
    )
    low_confidence_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence threshold below which to flag for review",
    )

    # Tool Configuration
    tool_confirmation_enabled: bool = Field(
        default=True,
        description="Whether to require confirmation for modification tools",
    )
    auto_execute_read_only: bool = Field(
        default=True,
        description="Auto-execute read-only tools without confirmation",
    )

    # GNORM Integration
    gnorm_api_url: str | None = Field(
        default=None,
        description="GNORM API base URL",
    )
    gnorm_api_key: str | None = Field(
        default=None,
        description="GNORM API authentication key",
    )
    gnorm_timeout: int = Field(
        default=30,
        description="GNORM API timeout in seconds",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )
    log_structured: bool = Field(
        default=True,
        description="Use structured logging format",
    )

    def validate_api_keys(self) -> None:
        """Validate that required API keys are present for the configured provider."""
        if self.llm_provider == LLMProvider.OPENAI and not self.openai_api_key:
            raise ValueError("OpenAI API key required when using OpenAI provider")
        if self.llm_provider == LLMProvider.ANTHROPIC and not self.anthropic_api_key:
            raise ValueError("Anthropic API key required when using Anthropic provider")

        if self.embedding_provider == EmbeddingProvider.OPENAI and not self.openai_api_key:
            raise ValueError("OpenAI API key required for OpenAI embeddings")


def load_config() -> AgentConfig:
    """Load configuration from environment and .env file."""
    return AgentConfig()

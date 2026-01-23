"""Tests for the GNORM integration module."""

from unittest.mock import AsyncMock, patch

import pytest

from itserr_agent.core.config import AgentConfig
from itserr_agent.integrations.gnorm import (
    GNORMAnnotation,
    GNORMClient,
    GNORMResponse,
    GNORMTool,
)
from itserr_agent.epistemic.indicators import IndicatorType


class TestGNORMClientConfiguration:
    """Tests for GNORM client configuration and fallback behavior."""

    def test_fallback_url_when_not_configured(self) -> None:
        """Client should use localhost:8000 when gnorm_api_url is None."""
        config = AgentConfig(gnorm_api_url=None)
        client = GNORMClient(config)

        # The fallback happens in _get_client, so we verify the config
        assert client.config.gnorm_api_url is None
        # Fallback is applied at client creation time in _get_client

    @pytest.mark.asyncio
    async def test_client_uses_fallback_url(self) -> None:
        """Client should use http://localhost:8000 when URL is not set."""
        config = AgentConfig(gnorm_api_url=None)
        client = GNORMClient(config)

        # Mock httpx.AsyncClient to capture the base_url
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_instance = AsyncMock()
            mock_client_class.return_value = mock_instance

            await client._get_client()

            # Verify the fallback URL was used
            mock_client_class.assert_called_once()
            call_kwargs = mock_client_class.call_args.kwargs
            assert call_kwargs["base_url"] == "http://localhost:8000"

    @pytest.mark.asyncio
    async def test_client_uses_configured_url(self) -> None:
        """Client should use configured URL when provided."""
        config = AgentConfig(gnorm_api_url="http://custom-gnorm:9000")
        client = GNORMClient(config)

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_instance = AsyncMock()
            mock_client_class.return_value = mock_instance

            await client._get_client()

            call_kwargs = mock_client_class.call_args.kwargs
            assert call_kwargs["base_url"] == "http://custom-gnorm:9000"

    def test_timeout_from_config(self) -> None:
        """Client should use timeout from config."""
        config = AgentConfig(gnorm_timeout=60)
        client = GNORMClient(config)
        assert client.config.gnorm_timeout == 60

    def test_default_timeout(self) -> None:
        """Client should use default timeout of 30 seconds."""
        config = AgentConfig()
        client = GNORMClient(config)
        assert client.config.gnorm_timeout == 30


class TestGNORMAnnotation:
    """Tests for GNORMAnnotation dataclass."""

    def test_epistemic_indicator_high_confidence(self) -> None:
        """High confidence annotations should be FACTUAL."""
        annotation = GNORMAnnotation(
            entity_text="Augustine",
            entity_type="person",
            start_offset=0,
            end_offset=9,
            confidence=0.92,
        )
        indicator = annotation.get_epistemic_indicator(high_confidence_threshold=0.85)
        assert indicator == IndicatorType.FACTUAL

    def test_epistemic_indicator_low_confidence(self) -> None:
        """Low confidence annotations should be INTERPRETIVE."""
        annotation = GNORMAnnotation(
            entity_text="the divine",
            entity_type="concept",
            start_offset=10,
            end_offset=20,
            confidence=0.65,
        )
        indicator = annotation.get_epistemic_indicator(high_confidence_threshold=0.85)
        assert indicator == IndicatorType.INTERPRETIVE

    def test_epistemic_indicator_at_threshold(self) -> None:
        """Annotations at exactly the threshold should be FACTUAL."""
        annotation = GNORMAnnotation(
            entity_text="Rome",
            entity_type="place",
            start_offset=0,
            end_offset=4,
            confidence=0.85,
        )
        indicator = annotation.get_epistemic_indicator(high_confidence_threshold=0.85)
        assert indicator == IndicatorType.FACTUAL

    def test_epistemic_indicator_custom_threshold(self) -> None:
        """Should respect custom threshold from config."""
        annotation = GNORMAnnotation(
            entity_text="Augustine",
            entity_type="person",
            start_offset=0,
            end_offset=9,
            confidence=0.88,
        )
        # With higher threshold, 0.88 becomes INTERPRETIVE
        indicator = annotation.get_epistemic_indicator(high_confidence_threshold=0.90)
        assert indicator == IndicatorType.INTERPRETIVE


class TestGNORMResponse:
    """Tests for GNORMResponse dataclass."""

    def test_response_with_annotations(self) -> None:
        """Response should contain list of annotations."""
        annotations = [
            GNORMAnnotation("Augustine", "person", 0, 9, 0.95),
            GNORMAnnotation("Hippo", "place", 13, 18, 0.87),
        ]
        response = GNORMResponse(
            annotations=annotations,
            text_id="test-001",
            processing_time_ms=150.5,
        )
        assert len(response.annotations) == 2
        assert response.text_id == "test-001"
        assert response.processing_time_ms == 150.5

    def test_response_empty_annotations(self) -> None:
        """Response can have empty annotations list."""
        response = GNORMResponse(annotations=[])
        assert len(response.annotations) == 0


class TestGNORMTool:
    """Tests for GNORMTool wrapper."""

    @pytest.fixture
    def mock_client(self) -> GNORMClient:
        """Create a mock GNORM client."""
        config = AgentConfig()
        return GNORMClient(config)

    @pytest.fixture
    def tool(self, mock_client: GNORMClient) -> GNORMTool:
        """Create a GNORM tool with mock client."""
        return GNORMTool(mock_client)

    def test_tool_name(self, tool: GNORMTool) -> None:
        """Tool should have correct name."""
        assert tool.name == "gnorm_annotate"

    def test_tool_description(self, tool: GNORMTool) -> None:
        """Tool should have meaningful description."""
        assert "GNORM" in tool.description
        assert "annotate" in tool.description.lower()

    def test_tool_category_is_external(self, tool: GNORMTool) -> None:
        """Tool should be categorized as EXTERNAL."""
        from itserr_agent.tools.base import ToolCategory

        assert tool.category == ToolCategory.EXTERNAL

    @pytest.mark.asyncio
    async def test_execute_without_text_fails(self, tool: GNORMTool) -> None:
        """Execute should fail when no text is provided."""
        result = await tool.execute()
        assert result.success is False
        assert "No text provided" in result.error_message

    @pytest.mark.asyncio
    async def test_execute_with_empty_text_fails(self, tool: GNORMTool) -> None:
        """Execute should fail when empty text is provided."""
        result = await tool.execute(text="")
        assert result.success is False
        assert "No text provided" in result.error_message


class TestGNORMClientContextManager:
    """Tests for GNORMClient async context manager."""

    @pytest.mark.asyncio
    async def test_context_manager_cleanup(self) -> None:
        """Context manager should clean up client on exit."""
        config = AgentConfig()

        async with GNORMClient(config) as client:
            # Client should be usable
            assert client is not None

        # After context exit, client should be closed
        assert client._client is None

    @pytest.mark.asyncio
    async def test_close_idempotent(self) -> None:
        """Calling close multiple times should be safe."""
        config = AgentConfig()
        client = GNORMClient(config)

        await client.close()
        await client.close()  # Should not raise
        assert client._client is None

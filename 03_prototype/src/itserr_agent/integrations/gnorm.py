"""
GNORM Integration - CRF-based annotation service client.

This module provides integration with the GNORM API from WP3,
enabling the agent to request and process named entity annotations
for religious and theological texts.

Note: API details to be confirmed during Feb 11-12 technical briefing.
"""

from dataclasses import dataclass
from typing import Any

import httpx
import structlog

from itserr_agent.core.config import AgentConfig
from itserr_agent.epistemic.indicators import IndicatorType
from itserr_agent.tools.base import BaseTool, ToolCategory, ToolResult

logger = structlog.get_logger()


@dataclass
class GNORMAnnotation:
    """
    A single annotation from GNORM.

    Attributes:
        entity_text: The text span that was annotated
        entity_type: The type of entity (person, place, concept, etc.)
        start_offset: Character offset where the entity starts
        end_offset: Character offset where the entity ends
        confidence: Confidence score (0.0 to 1.0)
        metadata: Additional annotation metadata
    """

    entity_text: str
    entity_type: str
    start_offset: int
    end_offset: int
    confidence: float
    metadata: dict[str, Any] | None = None

    @property
    def epistemic_indicator(self) -> IndicatorType:
        """
        Map confidence to epistemic indicator.

        High confidence (≥0.85) → FACTUAL
        Medium confidence → INTERPRETIVE
        """
        if self.confidence >= 0.85:
            return IndicatorType.FACTUAL
        else:
            return IndicatorType.INTERPRETIVE


@dataclass
class GNORMResponse:
    """Response from the GNORM API."""

    annotations: list[GNORMAnnotation]
    text_id: str | None = None
    processing_time_ms: float = 0.0
    model_version: str | None = None


class GNORMClient:
    """
    Client for the GNORM annotation API.

    Provides methods for requesting entity annotations and processing
    the results with appropriate epistemic indicators.

    Note: API details are placeholders pending technical briefing.
    """

    def __init__(self, config: AgentConfig) -> None:
        """
        Initialize the GNORM client.

        Args:
            config: Agent configuration containing GNORM settings
        """
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.config.gnorm_api_url or "http://localhost:8000",
                timeout=self.config.gnorm_timeout,
                headers=self._get_auth_headers(),
            )
        return self._client

    def _get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers if configured."""
        headers = {"Content-Type": "application/json"}
        if self.config.gnorm_api_key:
            # Auth mechanism TBD during briefing
            headers["Authorization"] = f"Bearer {self.config.gnorm_api_key}"
        return headers

    async def annotate(
        self,
        text: str,
        entity_types: list[str] | None = None,
        language: str = "en",
    ) -> GNORMResponse:
        """
        Request annotations for a text.

        Args:
            text: The text to annotate
            entity_types: Optional filter for specific entity types
            language: Text language code

        Returns:
            GNORMResponse containing annotations

        Raises:
            GNORMError: If the API request fails
        """
        client = await self._get_client()

        # Request payload (format TBD during briefing)
        payload = {
            "text": text,
            "language": language,
        }
        if entity_types:
            payload["entity_types"] = entity_types

        try:
            response = await client.post("/annotate", json=payload)
            response.raise_for_status()
            data = response.json()

            return self._parse_response(data)

        except httpx.HTTPError as e:
            logger.error("gnorm_api_error", error=str(e))
            raise GNORMError(f"GNORM API request failed: {e}") from e

    def _parse_response(self, data: dict[str, Any]) -> GNORMResponse:
        """Parse the API response into structured data."""
        # Response format TBD during briefing
        # This is a placeholder implementation
        annotations = []

        for item in data.get("annotations", []):
            annotations.append(
                GNORMAnnotation(
                    entity_text=item.get("text", ""),
                    entity_type=item.get("type", "unknown"),
                    start_offset=item.get("start", 0),
                    end_offset=item.get("end", 0),
                    confidence=item.get("confidence", 0.5),
                    metadata=item.get("metadata"),
                )
            )

        return GNORMResponse(
            annotations=annotations,
            text_id=data.get("text_id"),
            processing_time_ms=data.get("processing_time_ms", 0.0),
            model_version=data.get("model_version"),
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


class GNORMError(Exception):
    """Exception raised for GNORM API errors."""

    pass


class GNORMTool(BaseTool):
    """
    Tool wrapper for GNORM integration.

    Implements the external tool pattern with confirmation + first-time gate.
    """

    name = "gnorm_annotate"
    description = "Annotate text with GNORM CRF-based named entity recognition"
    category = ToolCategory.EXTERNAL

    def __init__(self, client: GNORMClient) -> None:
        """Initialize the tool with a GNORM client."""
        super().__init__()
        self._client = client

    async def execute(
        self,
        text: str,
        entity_types: list[str] | None = None,
        **kwargs: Any,
    ) -> ToolResult:
        """
        Execute GNORM annotation.

        Args:
            text: Text to annotate
            entity_types: Optional filter for entity types

        Returns:
            ToolResult containing annotations
        """
        try:
            response = await self._client.annotate(
                text=text,
                entity_types=entity_types,
            )

            return ToolResult(
                success=True,
                data={
                    "annotations": [
                        {
                            "text": a.entity_text,
                            "type": a.entity_type,
                            "confidence": a.confidence,
                            "indicator": a.epistemic_indicator.value,
                        }
                        for a in response.annotations
                    ],
                    "count": len(response.annotations),
                },
                tool_name=self.name,
                category=self.category,
                execution_time_ms=response.processing_time_ms,
            )

        except GNORMError as e:
            return ToolResult(
                success=False,
                data=None,
                tool_name=self.name,
                category=self.category,
                error_message=str(e),
            )

    def format_result(self, result: ToolResult) -> str:
        """Format GNORM results for presentation."""
        if not result.success:
            return f"GNORM annotation failed: {result.error_message}"

        data = result.data
        count = data.get("count", 0)

        if count == 0:
            return "No entities found in the text."

        lines = [f"Found {count} entities:"]
        for ann in data.get("annotations", []):
            indicator = ann.get("indicator", "INTERPRETIVE")
            lines.append(
                f"  [{indicator}] {ann['text']} ({ann['type']}, "
                f"confidence: {ann['confidence']:.0%})"
            )

        return "\n".join(lines)

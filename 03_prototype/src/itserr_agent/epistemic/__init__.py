"""
Epistemic module - Epistemic Modesty Indicators implementation.

This module implements the classification and tagging system for
differentiating response types:
- FACTUAL: Verifiable information with citations
- INTERPRETIVE: AI-assisted analysis requiring verification
- DEFERRED: Matters requiring human judgment
"""

from itserr_agent.epistemic.classifier import EpistemicClassifier
from itserr_agent.epistemic.indicators import EpistemicIndicator, IndicatorType

__all__ = [
    "EpistemicClassifier",
    "EpistemicIndicator",
    "IndicatorType",
]

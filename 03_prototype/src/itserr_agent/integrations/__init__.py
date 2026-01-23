"""
Integrations module - External service integrations.

This module contains integrations with ITSERR project tools:
- GNORM (WP3): CRF-based named entity recognition
- T-ReS (WP3): Text analysis and annotation
- Future: DaMSym (WP4), YASMINE (WP6), REVER (WP7)
"""

from itserr_agent.integrations.gnorm import GNORMClient

__all__ = [
    "GNORMClient",
]

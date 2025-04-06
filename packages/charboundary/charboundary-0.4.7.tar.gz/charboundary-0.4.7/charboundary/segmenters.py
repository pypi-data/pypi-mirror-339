"""
Text segmentation functionality for the charboundary library.

This module re-exports the main classes from the segmenters package.
"""

from charboundary.segmenters import (
    TextSegmenter,
    SegmenterConfig,
    TextSegmenterProtocol,
    MetricsResult,
    ParagraphSegmenter,
    SentenceSegmenter,
    SpanHandler,
)

__all__ = [
    "TextSegmenter",
    "SegmenterConfig",
    "TextSegmenterProtocol",
    "MetricsResult",
    "ParagraphSegmenter",
    "SentenceSegmenter",
    "SpanHandler",
]

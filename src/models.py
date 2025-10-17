"""Data models shared across the ingestion and query pipelines."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ScrapedDocument:
    """Raw HTML captured from a crawled page."""

    url: str
    title: str
    html: str


@dataclass
class MarkdownDocument:
    """Markdown representation of a scraped page saved to disk."""

    url: str
    title: str
    markdown: str
    output_path: Path


@dataclass
class DocumentChunk:
    """Chunked slice of markdown content prepared for embedding."""

    id: str
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]


@dataclass
class QueryResult:
    """Answer returned by the query engine along with supporting context."""

    answer: str
    relevant_chunks: List[DocumentChunk]
    iterations: int

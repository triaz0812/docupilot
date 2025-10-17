"""Ingestion pipeline that coordinates scraping, conversion, and indexing."""

from __future__ import annotations

from typing import Dict

from .chunking import chunk_markdown_documents
from .config import Settings
from .embedding_client import EmbeddingClient
from .markdown_converter import convert_documents
from .scraper import scrape_site
from .vector_store import ChromaVectorStore


class IngestionPipeline:
    """High-level workflow for turning a site into searchable embeddings."""

    def __init__(
        self,
        settings: Settings,
        embedder: EmbeddingClient,
        vector_store: ChromaVectorStore,
    ) -> None:
        """Prepare collaborators used across pipeline executions."""

        self._settings = settings
        self._embedder = embedder
        self._vector_store = vector_store

    def run(self, base_url: str) -> Dict[str, int]:
        """Scrape, convert, chunk, embed, and index the documentation site."""

        scraped = scrape_site(base_url, self._settings)
        markdown_docs = list(convert_documents(scraped, self._settings.scrape_output_dir))
        chunks = chunk_markdown_documents(markdown_docs)

        embeddings = self._embedder.embed_texts(chunk.content for chunk in chunks)
        self._vector_store.upsert(chunks, embeddings)

        return {
            "pages": len(scraped),
            "markdown_documents": len(markdown_docs),
            "chunks": len(chunks),
        }

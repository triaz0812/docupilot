"""ChromaDB vector-store integration for persisting document embeddings."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import chromadb
from chromadb.api.models.Collection import Collection

from .models import DocumentChunk


class ChromaVectorStore:
    """Encapsulates Chroma collection management and retrieval helpers."""

    def __init__(
        self,
        persist_directory: Path,
        collection_name: str = "documents",
    ) -> None:
        """Create or load a persistent Chroma collection."""

        persist_directory.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(persist_directory))
        self._collection: Collection = client.get_or_create_collection(
            collection_name
        )

    def upsert(self, chunks: Iterable[DocumentChunk], embeddings: List[List[float]]) -> None:
        """Add or update embeddings for the supplied document chunks."""

        chunk_list = list(chunks)
        if not chunk_list:
            return
        if len(chunk_list) != len(embeddings):
            raise ValueError("Mismatch between chunks and embeddings size")

        ids = [chunk.id for chunk in chunk_list]
        documents = [chunk.content for chunk in chunk_list]
        metadatas = [
            {
                "url": chunk.url,
                "title": chunk.title,
                "source": chunk.metadata.get("source"),
                "position": chunk.metadata.get("position"),
            }
            for chunk in chunk_list
        ]

        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
        )

    def query(self, query_embedding: List[float], top_k: int) -> List[DocumentChunk]:
        """Return the top-k stored chunks that best match the query embedding."""

        result = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        documents = result.get("documents", [[]])[0]
        ids = result.get("ids", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        chunks: List[DocumentChunk] = []
        for idx, doc in enumerate(documents):
            metadata = metadatas[idx] if idx < len(metadatas) else {}
            chunk_id = ids[idx] if idx < len(ids) else f"chunk-{idx}"
            chunks.append(
                DocumentChunk(
                    id=chunk_id,
                    url=metadata.get("url", ""),
                    title=metadata.get("title", ""),
                    content=doc,
                    metadata=metadata,
                )
            )
        return chunks

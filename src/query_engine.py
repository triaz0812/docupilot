"""Query orchestration that ties embeddings, retrieval, and LLM rewrites together."""

from __future__ import annotations

from typing import List

from .config import Settings
from .embedding_client import EmbeddingClient
from .llm_client import LLMClient
from .models import DocumentChunk, QueryResult
from .vector_store import ChromaVectorStore


class QueryEngine:
    """Answer user questions by iteratively refining retrieval and synthesis."""

    def __init__(
        self,
        settings: Settings,
        embedder: EmbeddingClient,
        llm: LLMClient,
        vector_store: ChromaVectorStore,
        max_iterations: int = 3,
    ) -> None:
        """Store the collaborating components used to answer questions."""

        self._settings = settings
        self._embedder = embedder
        self._llm = llm
        self._vector_store = vector_store
        self._max_iterations = max_iterations

    def ask(self, question: str) -> QueryResult:
        """Return an answer derived from the indexed corpus for the question."""

        attempts: List[str] = []
        current_query = question
        best_chunks: List[DocumentChunk] = []

        for iteration in range(1, self._max_iterations + 1):
            attempts.append(current_query)
            embedding = self._embed_query(current_query)
            if embedding is None:
                break

            chunks = self._vector_store.query(embedding, self._settings.top_k)
            if chunks and self._llm.assess_relevance(question, chunks):
                answer = self._llm.generate_answer(question, chunks)
                return QueryResult(
                    answer=answer,
                    relevant_chunks=chunks,
                    iterations=iteration,
                )

            best_chunks = chunks or best_chunks
            current_query = self._llm.rewrite_query(question, attempts)

        # Final attempt uses whichever chunks are most recent even if relevance failed.
        final_chunks = best_chunks
        if final_chunks:
            answer = self._llm.generate_answer(question, final_chunks)
        else:
            answer = "I could not find relevant information in the indexed documents."

        return QueryResult(
            answer=answer,
            relevant_chunks=final_chunks,
            iterations=self._max_iterations,
        )

    def _embed_query(self, query: str) -> List[float] | None:
        """Embed the query text and return the resulting vector when available."""

        embeddings = self._embedder.embed_texts([query])
        if not embeddings:
            return None
        return embeddings[0]

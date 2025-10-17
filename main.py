"""Command line entry points for the documentation RAG pipeline."""

from __future__ import annotations

import typer

from src.config import get_settings
from src.embedding_client import EmbeddingClient
from src.llm_client import LLMClient
from src.pipeline import IngestionPipeline
from src.query_engine import QueryEngine
from src.vector_store import ChromaVectorStore

app = typer.Typer(help="RAG pipeline for querying scraped technical documentation.")


@app.command()
def ingest(url: str) -> None:
    """Scrape a documentation site and index the content."""
    settings = get_settings()
    embedder = EmbeddingClient(settings)
    vector_store = ChromaVectorStore(
        settings.chroma_persist_dir, max_batch_size=settings.chroma_upsert_batch_size
    )
    pipeline = IngestionPipeline(settings, embedder, vector_store)

    stats = pipeline.run(url)
    typer.echo(f"Indexed {stats['pages']} pages into {stats['chunks']} chunks.")


@app.command()
def ask(
    question: str,
    show_sources: bool = typer.Option(True, help="Display source file references."),
) -> None:
    """Ask a question against the indexed documentation."""
    settings = get_settings()
    embedder = EmbeddingClient(settings)
    llm = LLMClient(settings)
    vector_store = ChromaVectorStore(
        settings.chroma_persist_dir, max_batch_size=settings.chroma_upsert_batch_size
    )
    engine = QueryEngine(settings, embedder, llm, vector_store)

    result = engine.ask(question)

    typer.echo("\nAnswer:\n")
    typer.echo(result.answer)

    if show_sources and result.relevant_chunks:
        typer.echo("\nSources:\n")
        for chunk in result.relevant_chunks:
            source = chunk.metadata.get("source", chunk.url)
            summary = chunk.content.strip().splitlines()[0][:120]
            typer.echo(
                f"- {source} (chunk {chunk.metadata.get('position', '?')}) :: {summary}"
            )


if __name__ == "__main__":
    app()

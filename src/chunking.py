"""Chunking helpers for splitting Markdown into embedding-ready slices."""

from __future__ import annotations

from typing import Iterable, List

from .models import DocumentChunk, MarkdownDocument


def chunk_markdown_document(
    document: MarkdownDocument,
    chunk_size: int = 1600,
    chunk_overlap: int = 200,
) -> List[DocumentChunk]:
    """Split a single Markdown document into overlapping chunks."""

    text = document.markdown
    chunks: List[DocumentChunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        chunk_id = f"{document.output_path.stem}-{index}"
        chunks.append(
            DocumentChunk(
                id=chunk_id,
                url=document.url,
                title=document.title,
                content=chunk_text,
                metadata={
                    "source": str(document.output_path),
                    "position": index,
                },
            )
        )
        index += 1
        start += max(chunk_size - chunk_overlap, 1)

    return chunks


def chunk_markdown_documents(
    documents: Iterable[MarkdownDocument],
    chunk_size: int = 1600,
    chunk_overlap: int = 200,
) -> List[DocumentChunk]:
    """Flatten the chunks produced for an iterable of Markdown documents."""

    all_chunks: List[DocumentChunk] = []
    for document in documents:
        all_chunks.extend(chunk_markdown_document(document, chunk_size, chunk_overlap))
    return all_chunks

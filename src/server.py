"""FastAPI server exposing the chat interface and static assets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import get_settings
from .embedding_client import EmbeddingClient
from .llm_client import LLMClient
from .query_engine import QueryEngine
from .vector_store import ChromaVectorStore

app = FastAPI(title="Doc RAG Chat", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_settings = get_settings()
_embedder = EmbeddingClient(_settings)
_llm = LLMClient(_settings)
_vector_store = ChromaVectorStore(
    _settings.chroma_persist_dir, max_batch_size=_settings.chroma_upsert_batch_size
)
_engine = QueryEngine(_settings, _embedder, _llm, _vector_store)

static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ChatRequest(BaseModel):
    """Inbound chat message payload."""

    message: str


class ChatResponse(BaseModel):
    """Structured response returned to the chat front end."""

    answer: str
    iterations: int
    sources: list[Dict[str, Any]]


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the static chat application shell."""

    index_path = static_dir / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="Front-end assets are missing.")
    return index_path.read_text(encoding="utf-8")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat questions by delegating to the query engine."""

    question = request.message.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        result = _engine.ask(question)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    sources = [
        {
            "source": chunk.metadata.get("source", chunk.url),
            "title": chunk.title,
            "position": chunk.metadata.get("position"),
            "url": chunk.url,
        }
        for chunk in result.relevant_chunks
    ]

    return ChatResponse(answer=result.answer, iterations=result.iterations, sources=sources)

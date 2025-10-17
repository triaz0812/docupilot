"""Lightweight wrapper around the OpenAI embeddings API."""

from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from .config import Settings


class EmbeddingClient:
    """Generate vector embeddings for text using the configured OpenAI model."""

    def __init__(self, settings: Settings) -> None:
        """Initialise the OpenAI client with the selected embedding model."""

        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.embed_model

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        """Return embeddings for the provided iterable of texts."""

        payload = list(texts)
        if not payload:
            return []
        response = self._client.embeddings.create(model=self._model, input=payload)
        return [item.embedding for item in response.data]

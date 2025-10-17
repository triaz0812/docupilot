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
        self._batch_size = settings.embed_batch_size

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        """Return embeddings for the provided iterable of texts."""

        payload = list(texts)
        if not payload:
            return []

        embeddings: List[List[float]] = []
        default_batch_size = max(1, self._batch_size)
        start = 0

        while start < len(payload):
            current_batch_size = min(default_batch_size, len(payload) - start)

            while current_batch_size > 0:
                batch = payload[start : start + current_batch_size]
                try:
                    response = self._client.embeddings.create(
                        model=self._model,
                        input=batch,
                    )
                except Exception as exc:  # noqa: BLE001
                    message = str(exc)
                    if (
                        "max batch size" in message.lower()
                        and current_batch_size > 1
                    ):
                        current_batch_size = max(1, current_batch_size // 2)
                        continue
                    raise

                embeddings.extend(item.embedding for item in response.data)
                start += current_batch_size
                default_batch_size = current_batch_size
                break

            if current_batch_size == 0:
                raise RuntimeError(
                    "Failed to create embeddings: batch size reduced to zero."
                )

        return embeddings

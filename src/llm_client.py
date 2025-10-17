"""Client utilities for interacting with the LLM during query flow."""

from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from .config import Settings
from .models import DocumentChunk


class LLMClient:
    """Wrapper around the chat completion API for RAG-specific prompts."""

    def __init__(self, settings: Settings) -> None:
        """Initialise the OpenAI chat client with the configured model."""

        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.llm_model

    def _run_chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """Execute a chat completion with the provided prompts."""

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def assess_relevance(self, question: str, chunks: Iterable[DocumentChunk]) -> bool:
        """Classify whether retrieved chunks appear relevant to the question."""

        context = "\n\n".join(
            f"Chunk {index + 1}:\n{chunk.content[:600]}"
            for index, chunk in enumerate(chunks)
        )
        user_prompt = (
            "You will be given a user question and retrieval snippets. "
            "Answer with 'relevant' if the snippets appear to answer the question, "
            "otherwise answer 'revise'.\n\n"
            f"Question: {question}\n\nSnippets:\n{context if context else 'None'}"
        )
        reply = self._run_chat(
            (
                "You are a strict classifier that answers with a single word: "
                "relevant or revise."
            ),
            user_prompt,
            temperature=0.0,
        )
        return reply.lower().startswith("relevant")

    def rewrite_query(self, question: str, previous_attempts: Iterable[str]) -> str:
        """Generate a refined retrieval query when earlier attempts failed."""

        attempts_text = "\n".join(previous_attempts)
        user_prompt = (
            "The current retrieval was not relevant. Rewrite the user's question "
            "to improve retrieval. Produce a concise, specific search query "
            "without extra commentary.\n\n"
            f"Original question: {question}\n"
            + (f"Past attempts:\n{attempts_text}" if attempts_text else "")
        )
        return self._run_chat(
            "You craft focused search queries for dense retrieval systems.",
            user_prompt,
            temperature=0.3,
        )

    def generate_answer(self, question: str, chunks: Iterable[DocumentChunk]) -> str:
        """Compose a grounded answer using the supplied supporting chunks."""

        context = "\n\n".join(
            (
                f"Source: {chunk.metadata.get('source', chunk.url)}\n"
                f"{chunk.content}"
            )
            for chunk in chunks
        )
        user_prompt = (
            "Use the provided context to answer the user's question. "
            "If the answer is not contained in the context, say you cannot answer "
            "confidently.\n\n"
            f"Question: {question}\n\nContext:\n"
            f"{context if context else 'No context provided.'}"
        )
        return self._run_chat(
            (
                "You are a knowledgeable technical assistant who only relies on the "
                "supplied context."
            ),
            user_prompt,
            temperature=0.2,
        )

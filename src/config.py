"""Configuration helpers for loading environment-driven settings."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime configuration settings derived from environment variables."""

    openai_api_key: str
    embed_model: str
    llm_model: str
    scrape_output_dir: Path
    chroma_persist_dir: Path
    max_chunks: int
    top_k: int
    scraper_user_agent: str
    scraper_timeout: int
    scraper_max_depth: int


def get_settings() -> Settings:
    """Construct application settings from environment variables."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Please add it to your environment or .env file."
        )

    scrape_output_dir = Path(
        os.getenv("SCRAPE_OUTPUT_DIR", "data/markdown")
    ).resolve()
    chroma_persist_dir = Path(
        os.getenv("CHROMA_PERSIST_DIR", "data/chroma_store")
    ).resolve()

    return Settings(
        openai_api_key=api_key,
        embed_model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-large"),
        llm_model=os.getenv("OPENAI_COMPLETION_MODEL", "gpt-4.1-mini"),
        scrape_output_dir=scrape_output_dir,
        chroma_persist_dir=chroma_persist_dir,
        max_chunks=int(os.getenv("MAX_CHUNKS", "8")),
        top_k=int(os.getenv("TOP_K", "4")),
        scraper_user_agent=os.getenv(
            "SCRAPER_USER_AGENT",
            "DocRAGBot/0.1 (+https://example.com/contact)",
        ),
        scraper_timeout=int(os.getenv("SCRAPER_TIMEOUT", "20")),
        scraper_max_depth=int(os.getenv("SCRAPER_MAX_DEPTH", "3")),
    )

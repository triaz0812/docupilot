"""Utilities for converting scraped HTML into Markdown files."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from markdownify import markdownify as to_markdown

from .models import MarkdownDocument, ScrapedDocument

_MARKDOWN_EXT = ".md"


def _slugify(text: str) -> str:
    """Return a filesystem-friendly slug derived from the source text."""

    slug = re.sub(r"[^a-zA-Z0-9-]+", "-", text.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "document"


def _sanitize_soup(soup: BeautifulSoup, base_url: str) -> None:
    """Strip unsupported tags and normalize asset references in-place."""

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            img.decompose()
            continue
        absolute_src = urljoin(base_url, src)
        img["src"] = absolute_src
        if not img.get("alt"):
            img["alt"] = Path(absolute_src).name


def _build_front_matter(document: ScrapedDocument) -> str:
    """Compose YAML front matter capturing source metadata."""

    return f"---\ntitle: \"{document.title}\"\nsource_url: {document.url}\n---\n\n"


def convert_documents(
    documents: Iterable[ScrapedDocument],
    output_dir: Path,
) -> Iterable[MarkdownDocument]:
    """Yield Markdown documents converted from scraped HTML pages."""

    output_dir.mkdir(parents=True, exist_ok=True)
    slug_counts: Dict[str, int] = {}

    for document in documents:
        soup = BeautifulSoup(document.html, "html.parser")
        _sanitize_soup(soup, document.url)

        markdown_body = to_markdown(
            str(soup),
            heading_style="ATX",
            strip="""iframe canvas""",
            bullets="*",
            code_language=True,
        ).strip()

        front_matter = _build_front_matter(document)
        markdown = front_matter + markdown_body + "\n"

        base_slug = _slugify(document.title or document.url)
        count = slug_counts.get(base_slug, 0)
        slug_counts[base_slug] = count + 1
        slug = base_slug if count == 0 else f"{base_slug}-{count}"
        output_path = output_dir / f"{slug}{_MARKDOWN_EXT}"
        output_path.write_text(markdown, encoding="utf-8")

        yield MarkdownDocument(
            url=document.url,
            title=document.title,
            markdown=markdown,
            output_path=output_path,
        )

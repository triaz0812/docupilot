"""Depth-limited web scraper used to collect documentation pages."""

from __future__ import annotations

from collections import deque
from typing import List, Set, Tuple
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

from .config import Settings
from .models import ScrapedDocument


class ScrapeError(RuntimeError):
    """Raised when a page cannot be fetched during crawling."""


def _normalize_url(url: str) -> str:
    """Collapse fragments and trailing slash for consistent URL comparison."""

    cleaned, _ = urldefrag(url)
    return cleaned.rstrip("/")


def _is_html(content_type: str | None) -> bool:
    """Return True when the content type header indicates HTML payload."""

    if not content_type:
        return False
    return "text/html" in content_type


def _extract_links(soup: BeautifulSoup, current_url: str, allowed_netloc: str) -> Set[str]:
    """Collect in-domain absolute links from an HTML document."""

    links: Set[str] = set()
    for anchor in soup.find_all("a", href=True):
        candidate = anchor.get("href")
        if not candidate:
            continue
        absolute = _normalize_url(urljoin(current_url, candidate))
        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"}:
            continue
        if parsed.netloc != allowed_netloc:
            continue
        links.add(absolute)
    return links


def scrape_site(base_url: str, settings: Settings) -> List[ScrapedDocument]:
    """Breadth-first crawl the base URL up to the configured depth."""

    base_url = _normalize_url(base_url)
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("base_url must be an http or https URL")

    queue: deque[Tuple[str, int]] = deque([(base_url, 0)])
    visited: Set[str] = set()
    documents: List[ScrapedDocument] = []
    session = requests.Session()

    while queue:
        current_url, depth = queue.popleft()
        if current_url in visited:
            continue

        try:
            response = session.get(
                current_url,
                headers={"User-Agent": settings.scraper_user_agent},
                timeout=settings.scraper_timeout,
            )
        except requests.RequestException as exc:
            raise ScrapeError(f"Failed to fetch {current_url}: {exc}") from exc

        if not _is_html(response.headers.get("Content-Type")):
            visited.add(current_url)
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else current_url
        )
        documents.append(
            ScrapedDocument(
                url=current_url,
                title=title,
                html=response.text,
            )
        )
        visited.add(current_url)

        if depth < settings.scraper_max_depth:
            for link in _extract_links(soup, current_url, parsed.netloc):
                if link not in visited:
                    queue.append((link, depth + 1))

    return documents

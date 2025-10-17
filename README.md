# Technical Documentation Query Application

This project builds a retrieval-augmented generation (RAG) pipeline that scrapes a technical documentation site, converts content to Markdown, indexes dense embeddings with ChromaDB, and serves query answers grounded strictly in the ingested corpus. The system automatically rewrites queries if retrieval results are weak, ensuring the LLM only answers when relevant supporting context is found.

## Key Capabilities

- Scrapes a seed URL and follows in-domain links up to three hops deep (configurable).
- Converts HTML pages to Markdown while preserving headings, lists, tables, and images.
- Splits Markdown into overlapping chunks and generates OpenAI embeddings.
- Stores embeddings locally with a persistent ChromaDB collection for fast semantic search.
- Uses an LLM to assess retrieval relevance, rewrite poor queries, and synthesize final answers backed by source snippets.
- Provides a responsive web chat interface with clear-chat controls that adapts to desktop and mobile screens.

## Project Structure

```
.
├── main.py                 # Typer CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── static/                 # Front-end assets for chat UI
├── src/
│   ├── chunking.py
│   ├── config.py
│   ├── embedding_client.py
│   ├── llm_client.py
│   ├── markdown_converter.py
│   ├── models.py
│   ├── pipeline.py
│   ├── query_engine.py
│   └── scraper.py
└── data/
    └── markdown/           # Markdown exports
```

## Setup

1. **Python**: Install Python 3.11+.
2. **Environment**: Create a virtual environment and install dependencies:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configuration**: Copy `.env.example` to `.env` and provide real values:
   - `OPENAI_API_KEY`: Required for embeddings and chat completions.
   - Optional overrides for embedding batch size (`EMBED_BATCH_SIZE`), Chroma upsert batching (`CHROMA_UPSERT_BATCH_SIZE`), scrape depth (`SCRAPER_MAX_DEPTH`), scrape output, or Chroma persistence paths.

   ### Version Control Setup

   The repository already includes a Python-focused `.gitignore`. To initialise version control:

   ```cmd
   git init
   git add .
   git commit -m "Initial commit"
   ```

   Sensitive configuration should live in `.env`, which is ignored by git. Share `.env.example` instead when collaborating.

## Usage

### Ingest Documentation

```cmd
python main.py ingest "https://docs.example.com"
```

The command scrapes the site (following in-domain links to the configured depth), exports Markdown into `data/markdown`, generates embeddings, and indexes them in `data/chroma_store`.

### Ask Questions

```cmd
python main.py ask "How do I authenticate requests?"
```

The CLI prints an answer grounded in the retrieved documentation along with the supporting sources used.

### Start the Chat Front End

```cmd
uvicorn src.server:app --reload
```

Open <http://127.0.0.1:8000/> to use the responsive browser-based chat interface.

### Docker Deployment

Build and run the application inside a container:

```cmd
docker build -t doc-rag .
docker run --rm -p 8000:8000 --env-file .env -v "%cd%\data":/app/data doc-rag
```

Alternatively, use Docker Compose (recommended for local development):

```cmd
docker compose up --build
```

The compose file mounts `./data` so embeddings persist across container restarts. To ingest documents inside the container, run:

```cmd
docker compose run --rm app python main.py ingest "https://docs.example.com"
```

Once ingestion completes, start the chat front end with `docker compose up` and browse to <http://127.0.0.1:8000/>.

## Notes

- Respect target site terms of service and add a contact URL to `SCRAPER_USER_AGENT`.
- The scraper limits traversal to three-level-deep in-domain links by default; adjust `SCRAPER_MAX_DEPTH` if you need more or less coverage.
- Large corpora can exceed Chroma's internal batching limit; tune `CHROMA_UPSERT_BATCH_SIZE` if you encounter related errors.
- ChromaDB persistence keeps your index across runs; delete `data/chroma_store` to rebuild from scratch.

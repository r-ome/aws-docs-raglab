# Current Status

Keep this file tiny and current.

## Current milestone

Milestone 4: retrieval + generation.

## What works

- Basic package structure exists under `app/`.
- `config.py` loads settings from `.env` via pydantic-settings (db_path, source_config_path, raw_data_dir, normalized_data_dir, chunk_size, chunk_overlap, embedding_model, chroma_path).
- SQLite init creates `data/sqlite/` and bootstraps `documents`, `document_versions`, `chunks`, and `schema_migrations` tables with foreign keys enabled.
- Typer CLI exposes `init`, `sync`, `ask`, `healthcheck`, `show-config`, and `sources`.
- FastAPI app wires `/query/ask` plus `/health`; startup calls `init_db()`.
- Source allowlist loading works from `sources/aws_sources.yaml`.
- Fetcher downloads a single page via httpx with timeout. Returns typed `FetchResult`.
- HTML extraction via BeautifulSoup (`html_parser.py`).
- Normalizer collapses whitespace and deduplicates blank lines.
- Content hashing via SHA-256 on normalized text.
- Raw HTML saved to `data/raw/`, normalized text saved to `data/normalized/`.
- Source records stored in SQLite `documents`, version history in `document_versions`.
- Sync compares latest content hash per document; classifies pages as new, changed, or unchanged.
- File writes only happen for new or changed documents (unchanged docs skip persistence).
- CLI `sync` command loops through all enabled sources with error handling and status reporting.
- Chunker splits normalized text into paragraph-aware windows with configurable size and overlap.
- Embedder generates vectors locally via sentence-transformers (`all-MiniLM-L6-v2`, 384 dimensions).
- Chroma vector store persists embeddings to `data/chroma/` with cosine similarity.
- Index service orchestrates chunk → embed → upsert for new/changed docs, deletes stale vectors before re-indexing.
- Chunk metadata stored in SQLite `chunks` table linked to `documents` and `document_versions`.
- 12 documents indexed, 75 vectors in Chroma.
- Retrieval layer can query Chroma for top-k chunks and build grounded prompt context.
- Ollama generation client is wired through an answer service.
- CLI `ask` command and `/query/ask` route now call the retrieval + generation pipeline.
- Milestones 2 and 3 are complete.

## What's next

- Add guardrails in retrieval for empty Chroma collections and low-result cases.
- Improve answer grounding, citation formatting, and abstention behavior.
- Add retrieval and generation tests.
- Expose more retrieval/debug details when needed (retrieved chunks, scores, prompt size).

## Open issues

- `pyproject.toml` currently requires Python `>=3.14.1`, matching the plan's `Python 3.14.1+`.
- DB migration handling for older local schemas is still deferred.
- HTML parser pulls in boilerplate (nav text, footer) — could be cleaned up in normalizer.
- Retrieval path still needs stronger guardrails around empty collections and query edge cases.

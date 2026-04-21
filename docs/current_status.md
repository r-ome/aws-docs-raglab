# Current Status

Keep this file tiny and current.

## Current milestone

Milestone 3: chunking, embeddings, and indexing, just started.

## What works

- Basic package structure exists under `app/`.
- `config.py` loads `db_path` and `source_config_path` from `.env` via pydantic-settings.
- SQLite init creates `data/sqlite/` and bootstraps `documents`, `document_versions`, `chunks`, and `schema_migrations` tables.
- Typer CLI exposes `init`, `sync`, `ask`, `healthcheck`, `show-config`, and `sources`.
- FastAPI app wires `/query/ask` plus `/health`; startup calls `init_db()`.
- Source allowlist loading works from `sources/aws_sources.yaml`.
- Fetcher downloads a single page via httpx with timeout.
- HTML extraction via BeautifulSoup (`html_parser.py`).
- Normalizer collapses whitespace and deduplicates blank lines.
- Content hashing via SHA-256 on normalized text.
- Raw HTML saved to `data/raw/`.
- Normalized text saved to `data/normalized/`.
- Source records are stored in SQLite `documents`.
- Fetch/version history is stored in SQLite `document_versions`, including `raw_path`, `normalized_path`, and `content_hash`.
- Sync compares the latest stored content hash per document; classifies pages as new, changed, or unchanged.
- CLI `sync` command loops through all enabled sources with error handling and status reporting.
- Milestone 2 core sync pipeline is complete end to end.
- Milestone 3 scaffolding exists for chunking and embeddings.

## What's next

- Build a chunker for normalized document text (`app/indexing/chunker.py`).
- Add local embedding generation (`app/indexing/embedder.py`).
- Add Chroma vector storage and upsert flow (`app/indexing/vector_store.py`).
- Build index service to orchestrate chunk → embed → upsert for new/changed docs only (`app/indexing/index_service.py`).
- Wire chunking into the normalized document pipeline.
- Persist chunk rows in SQLite and connect them to `document_versions`.

## Open issues

- `pyproject.toml` currently requires Python `>=3.14.1`, matching the plan's `Python 3.14.1+`.
- DB migration handling for older local schemas is still deferred.
- Vector store integration and indexing orchestration are not implemented yet.

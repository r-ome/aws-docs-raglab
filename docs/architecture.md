# Architecture

This document describes how the system is structured and how the pieces connect.

## Overview

The system is a local RAG pipeline with four layers:

1. **Source sync** — fetches, normalizes, and versions AWS documentation
2. **Indexing** — chunks documents, generates embeddings, stores vectors
3. **Retrieval + generation** — finds relevant chunks and generates grounded answers
4. **Interface** — CLI and API that call into shared service modules

Each layer is a separate package under `app/`. The CLI and API are thin wrappers — business logic lives in service modules.

## Data flow

```
sources/aws_sources.yaml
        |
        v
   [ Fetcher ]  ──>  data/raw/{doc_id}.html
        |
        v
   [ Normalizer ]  ──>  data/normalized/{doc_id}.txt
        |
        v
   [ Hasher ]  ──>  SHA-256 content hash
        |
        v
   [ SQLite ]  ──>  documents + document_versions tables
        |
        v  (only new/changed docs)
   [ Chunker ]  ──>  paragraph-aware text windows
        |
        v
   [ Embedder ]  ──>  384-dim vectors (all-MiniLM-L6-v2)
        |
        v
   [ Chroma ]  ──>  data/chroma/ (cosine similarity)
        |
        v  (at query time)
   [ Retriever ]  ──>  top-k chunks filtered by distance
        |
        v
   [ Context builder ]  ──>  numbered prompt with sources
        |
        v
   [ Ollama LLM ]  ──>  grounded answer with citations
```

## Package structure

### `app/config.py`

Central settings loaded from `.env` via pydantic-settings. All configurable values (paths, model names, thresholds) live here with sensible defaults.

### `app/db.py`

SQLite bootstrap. Creates tables (`documents`, `document_versions`, `chunks`, `schema_migrations`) with foreign keys enabled. Called on app startup.

### `app/ingestion/`

- `fetcher.py` — downloads a page via httpx, returns a typed `FetchResult`
- `html_parser.py` — extracts text from HTML using BeautifulSoup
- `normalizer.py` — collapses whitespace, deduplicates blank lines
- `storage.py` — persists raw HTML and normalized text to disk, writes metadata to SQLite
- `sync.py` — orchestrates fetch → normalize → hash → compare → store for each source

### `app/indexing/`

- `chunker.py` — splits text into paragraph-aware windows with configurable size and overlap
- `embedder.py` — generates vectors using sentence-transformers
- `vector_store.py` — Chroma wrapper for upsert, delete, and query
- `index_service.py` — orchestrates chunk → embed → upsert; deletes stale vectors before re-indexing

### `app/retrieval/`

- `retriever.py` — embeds the query, queries Chroma for top-k, filters by max distance
- `context_builder.py` — formats retrieved chunks into a numbered prompt with source URLs

### `app/generation/`

- `llm_client.py` — sends prompts to Ollama via HTTP, returns the response
- `answer_service.py` — ties retrieval and generation together; handles abstention, error handling, debug output

### `app/evals/`

- `runner.py` — feeds a JSONL dataset through the ask pipeline, saves results
- `scoring.py` — scores each result on source hits, keyword coverage, abstention, citations
- `report.py` — aggregates scores by category and prints a summary

### `app/cli/main.py`

Typer CLI. Commands: `init`, `sync`, `ask`, `eval`, `healthcheck`, `show-config`, `sources`. Each command calls into the service modules above.

### `app/api/main.py`

FastAPI app. Routes: `GET /health`, `POST /query/ask`. Calls the same service modules as the CLI.

## Storage

Most local data lives under `data/` and is gitignored. The eval dataset is tracked because it is project source material.

| Path | What | Format |
|---|---|---|
| `data/eval_dataset.jsonl` | Eval questions | JSONL |
| `data/raw/` | Original HTML from fetches | `.html` files |
| `data/normalized/` | Cleaned text | `.txt` files |
| `data/sqlite/raglab.db` | Document metadata, versions, chunks | SQLite |
| `data/chroma/` | Vector embeddings + stored text | Chroma persistent storage |
| `data/eval_results/` | Eval run outputs | JSONL |

## Incremental sync

The key architectural decision. On each sync:

1. Fetch and normalize the document
2. Hash the normalized text (SHA-256)
3. Compare against the latest stored version in SQLite
4. If unchanged — skip everything downstream
5. If new or changed — store new version, delete old vectors, re-chunk, re-embed, upsert

This means re-running `sync` is cheap when nothing changed, and only the affected documents get reprocessed when something did.

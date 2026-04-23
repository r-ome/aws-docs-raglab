# Current Status

Keep this file tiny and current.

## Current milestone

Milestone 6: polish and GitHub readiness.

## What works

- Basic package structure exists under `app/`.
- `config.py` loads settings from `.env` via pydantic-settings (db_path, source_config_path, raw_data_dir, normalized_data_dir, chunk_size, chunk_overlap, embedding_model, chroma_path, top_k, max_distance, min_chunks_for_answer, debug).
- SQLite init creates `data/sqlite/` and bootstraps `documents`, `document_versions`, `chunks`, and `schema_migrations` tables with foreign keys enabled.
- Typer CLI exposes `init`, `sync`, `ask`, `healthcheck`, `show-config`, `sources`, and `eval`.
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
- Retrieval filters chunks by max distance threshold to drop weak matches.
- Abstention: min chunk count gate skips generation when evidence is thin; prompt reinforces abstention behavior.
- Citation formatting returns numbered refs with title and URL, matching the reference numbers in the LLM prompt.
- Ollama error handling returns a structured error response instead of crashing.
- Debug mode exposes retrieved chunks, distances, ranks, and prompt length when `debug=True`.
- Eval dataset with 56 questions across factual, paraphrase, synthesis, ambiguous, and out-of-scope categories.
- Eval runner feeds questions through the ask pipeline and saves results to JSONL.
- Scoring checks source hit rate, keyword coverage, abstention correctness, and citation presence.
- Report aggregates scores by category and prints a summary.
- CLI `eval` command runs the full eval cycle in one shot.
- Milestones 1–6 are complete.

## What's next

- Add example screenshots or a short demo walkthrough.
- Optional: add DB migrations for older local schemas.
- Optional: improve HTML extraction to remove more AWS navigation boilerplate.

## Open issues

- `pyproject.toml` currently requires Python `>=3.14.1`, matching the plan's `Python 3.14.1+`.
- DB migration handling for older local schemas is still deferred.
- HTML parser pulls in boilerplate (nav text, footer) — could be cleaned up in normalizer.

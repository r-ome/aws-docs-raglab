# AWS Docs RAG Lab

A local-first RAG (Retrieval-Augmented Generation) system over curated AWS documentation. Fetches AWS docs, indexes them incrementally, and answers questions using a local LLM with source citations.

Built as a portfolio project to demonstrate document ingestion pipelines, incremental sync, vector search, and grounded generation — without relying on cloud AI services.

## What it does

1. **Fetches** a curated allowlist of AWS documentation pages
2. **Normalizes** HTML content into clean text
3. **Detects changes** via content hashing — only reprocesses what changed
4. **Chunks and embeds** documents locally using sentence-transformers
5. **Stores vectors** in a local Chroma database
6. **Answers questions** using a local Ollama model, grounded in retrieved context
7. **Cites sources** so you can verify answers against the original docs

## Stack

- **Python 3.14.1+**
- **FastAPI** — API layer
- **Typer** — CLI
- **Ollama** — local LLM for generation
- **sentence-transformers** — local embeddings (`all-MiniLM-L6-v2`)
- **ChromaDB** — vector storage
- **SQLite** — document metadata and version tracking
- **httpx** — HTTP fetching
- **BeautifulSoup** — HTML extraction
- **pydantic-settings** — configuration

## Setup

### Prerequisites

- Python 3.14.1+
- [Ollama](https://ollama.com) installed and running
- uv or pip

### Install

```bash
# clone the repo
git clone https://github.com/your-username/aws-docs-rag-lab.git
cd aws-docs-rag-lab

# install dependencies
uv sync  # or: pip install -e .

# pull an Ollama model
ollama pull mistral
```

### Configure

Copy `.env.example` to `.env` and adjust if needed. Most paths have sensible defaults; the main requirement is a working Ollama setup with the configured model available locally.

### Initialize

```bash
raglab init
```

This creates the SQLite database and data directories.

## Usage

### Sync documents

Fetch and process all enabled sources from the allowlist:

```bash
raglab sync
```

Re-running `sync` only reprocesses documents whose content has changed.

### Ask a question

```bash
raglab ask "How does Amazon Bedrock handle model invocation?"
```

### API

Start the FastAPI server:

```bash
uvicorn app.api.main:app --reload
```

Then hit the endpoints:

- `GET /health` — health check
- `POST /query/ask` — ask a question

### Run evals

```bash
raglab eval
```

Runs all questions from the eval dataset through the pipeline, scores the results, and prints a report.

### Other CLI commands

```bash
raglab healthcheck    # check system health
raglab show-config    # print current config
raglab sources        # list configured sources
```

### Running tests

```bash
uv run pytest tests/ -v
```

## How incremental sync works

The system hashes normalized document content (not raw HTML). On each sync:

1. Fetch the page
2. Extract and normalize text
3. Compute SHA-256 hash
4. Compare against the latest stored version
5. If unchanged — skip. If new or changed — store new version, re-chunk, re-embed

Changed documents have their old vectors deleted before new ones are upserted. This keeps the index clean without needing chunk-level diffing.

## Project structure

```
aws-docs-rag-lab/
├── app/
│   ├── config.py              # settings via pydantic-settings
│   ├── db.py                  # SQLite bootstrap
│   ├── ingestion/             # fetch, parse, normalize, sync
│   ├── indexing/              # chunk, embed, vector store
│   ├── retrieval/             # query, context building
│   ├── generation/            # LLM client, prompts, answer service
│   ├── api/                   # FastAPI routes
│   └── cli/                   # Typer commands
├── sources/
│   └── aws_sources.yaml       # curated URL allowlist
├── data/                      # local generated data is gitignored
│   ├── eval_dataset.jsonl     # tracked eval questions
│   ├── raw/                   # raw HTML
│   ├── normalized/            # cleaned text
│   ├── chroma/                # vector store
│   └── sqlite/                # metadata DB
├── docs/
│   ├── architecture.md        # system design and data flow
│   ├── tradeoffs.md           # design decisions and reasoning
│   ├── local_setup.md         # detailed setup guide
│   ├── project_plan.md
│   └── current_status.md
└── tests/
```

## Roadmap

- [x] **Milestone 1** — Scaffold and local runtime (repo structure, config, SQLite, CLI + API entrypoints)
- [x] **Milestone 2** — Document sync and normalization (fetcher, HTML extraction, content hashing, version tracking)
- [x] **Milestone 3** — Chunking, embeddings, and indexing (paragraph-aware chunker, sentence-transformers, Chroma upsert/delete)
- [x] **Milestone 4** — Retrieval and generation (top-k retrieval, grounded prompts, Ollama generation, citations, abstention)
- [x] **Milestone 5** — Evals (56-question dataset, eval runner, retrieval + answer quality scoring)
- [x] **Milestone 6** — Polish and GitHub readiness (tests, docs, architecture notes, tradeoffs)

### Future ideas

- Hybrid retrieval and reranking
- Metadata filtering on queries
- Scheduled background refresh
- Lightweight frontend
- Support for more doc types (PDFs, API references)
- Docker packaging
- Chunk-level incremental indexing

## Docs

- [Architecture](docs/architecture.md) — system design, data flow, package breakdown
- [Tradeoffs](docs/tradeoffs.md) — design decisions and reasoning
- [Local setup](docs/local_setup.md) — detailed setup and troubleshooting guide
- [Project plan](docs/project_plan.md) — full milestone plan and data model

## Current status

All 6 milestones are complete. The pipeline works end-to-end: sync, indexing, retrieval, generation, and evals. See [docs/current_status.md](docs/current_status.md) for details.

## License

MIT

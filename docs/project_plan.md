# AWS Docs RAG Lab with Incremental Sync — Project Plan

This is the project reference document for the repo.

- Update this file whenever implementation meaningfully changes.
- Use this plan as the default source of truth for architecture, scope, and priorities during implementation and review.
- If the code intentionally differs from this plan, document the reason in review notes or adjacent docs.

See also: [current_status.md](/Users/jeromeagapay/Documents/aws-docs-rag-lab/docs/current_status.md)

## Goal

Build a serious local-first Python portfolio project that demonstrates:

- local LLM usage
- local embedding model usage
- vector database usage
- document ingestion
- AWS docs scraping/fetching
- incremental sync and selective re-indexing
- RAG query pipeline
- basic evals
- good software engineering structure

This should feel like a mini production ingestion + retrieval system, not a toy chatbot.

## Product concept

The app is a local RAG assistant over a curated set of AWS and Amazon Bedrock documentation.

It should:

1. fetch a curated allowlist of AWS docs/pages/blog posts
2. normalize content
3. detect changed documents using content hashes
4. only reprocess changed docs
5. store vectors locally
6. answer questions with a local LLM
7. cite source URLs/chunks
8. include a small eval dataset and evaluation runner

## Scope constraints

- Python as the main language
- local-first, runnable on a normal developer machine
- curated allowlist of URLs only
- keep scope realistic and GitHub-friendly
- prefer simplicity and clarity over framework complexity
- prioritize HTML/doc pages over PDFs in V1

## Recommended stack

- Python 3.14.1+
- FastAPI for API
- Typer for CLI
- Ollama for local generation
- sentence-transformers for local embeddings
- Chroma for local vector storage
- SQLite for document metadata, version tracking, and eval runs
- httpx for fetching
- BeautifulSoup / readability-lxml / trafilatura for extraction
- pytest for tests
- pydantic-settings for config

## Architecture

The system has 4 parts:

### 1. Source sync pipeline

- read allowed sources from config
- fetch documents
- extract readable text
- normalize content
- compute normalized content hash
- store fetch/version metadata in SQLite
- mark each doc as new, changed, unchanged, or failed

### 2. Indexing pipeline

- process only new or changed documents
- chunk normalized content
- attach metadata to chunks
- generate embeddings locally
- upsert vectors into Chroma
- remove stale vectors for changed docs before re-indexing

### 3. Query pipeline

- embed the user query locally
- retrieve top-k chunks from vector store
- build grounded context
- call local LLM through Ollama
- return answer with citations
- abstain when evidence is weak

### 4. Interface/observability layer

- CLI first, API second
- inspect docs, retrieved chunks, and sync status
- log changed vs skipped docs
- optionally expose retrieval scores and prompt/context size estimates

## Key design principles

### Real pipeline thinking

Treat this as a small ingestion + indexing + retrieval system.

### Incremental indexing

This is a main differentiator:

- content hashing
- idempotent refreshes
- selective re-indexing
- version-aware metadata

### Clean Python architecture

Business logic should live in service/modules, not inside CLI or route handlers.

### Interview-friendly tradeoffs

Optimize for:

- local development
- low compute cost
- clarity
- extensibility
- debuggability

## Repository structure

```text
aws-docs-rag-lab/
├─ README.md
├─ pyproject.toml
├─ .env.example
├─ Makefile
├─ sources/
│  └─ aws_sources.yaml
├─ app/
│  ├─ config.py
│  ├─ db.py
│  ├─ logging.py
│  ├─ models/
│  ├─ ingestion/
│  │  ├─ fetcher.py
│  │  ├─ normalizer.py
│  │  ├─ parser_html.py
│  │  ├─ hashing.py
│  │  ├─ sync_service.py
│  │  └─ storage.py
│  ├─ indexing/
│  │  ├─ chunker.py
│  │  ├─ embedder.py
│  │  ├─ vector_store.py
│  │  ├─ index_service.py
│  │  └─ ids.py
│  ├─ retrieval/
│  │  ├─ retriever.py
│  │  ├─ rankers.py
│  │  ├─ context_builder.py
│  │  └─ citations.py
│  ├─ generation/
│  │  ├─ llm_client.py
│  │  ├─ prompts.py
│  │  ├─ answer_service.py
│  │  └─ guards.py
│  ├─ evals/
│  │  ├─ dataset.py
│  │  ├─ runner.py
│  │  ├─ scoring.py
│  │  └─ report.py
│  ├─ api/
│  │  ├─ main.py
│  │  ├─ routes_query.py
│  │  ├─ routes_docs.py
│  │  └─ routes_admin.py
│  └─ cli/
│     └─ main.py
├─ data/
│  ├─ raw/
│  ├─ normalized/
│  ├─ manifests/
│  ├─ chroma/
│  ├─ eval_results/
│  └─ sqlite/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ fixtures/
└─ docs/
   ├─ architecture.md
   ├─ tradeoffs.md
   ├─ local_setup.md
   ├─ eval_method.md
   └─ project_plan.md
```

## Milestones

### Milestone 1: scaffold and local runtime

Goal: make the project boot cleanly.

Build:

- repo structure
- `pyproject.toml`
- config system
- logging
- SQLite init
- CLI entrypoint
- FastAPI entrypoint
- healthcheck/init command
- `/health` route

Definition of done:

- CLI runs
- FastAPI starts
- config loads
- DB initializes

### Milestone 2: document sync + normalization

Build:

- source config loader
- allowlist YAML
- fetcher with timeout/retry/user-agent
- HTML extraction and normalization
- raw and normalized file persistence
- content hashing
- document + version metadata tables
- sync status reporting

Definition of done:

- `sync` fetches documents
- changed vs unchanged is tracked

### Milestone 3: chunking + embeddings + indexing

Build:

- chunker with overlap
- embedding client
- Chroma integration
- chunk metadata persistence
- delete stale vectors for changed docs
- upsert fresh vectors

Definition of done:

- changed docs can be indexed locally

### Milestone 4: retrieval + generation

Build:

- query embedding
- top-k retrieval
- context builder
- Ollama LLM client
- grounded prompt
- citation formatting
- abstention behavior

Definition of done:

- `ask` returns grounded answers with citations

### Milestone 5: evals

Build:

- eval dataset format
- 25-50 questions
- eval runner
- result saving
- manual-review-friendly outputs
- simple retrieval and answer quality fields

Definition of done:

- eval script produces structured results

### Milestone 6: polish and GitHub readiness

Build:

- tests
- docs
- README
- demo commands
- architecture notes
- tradeoff explanations
- example screenshots or walkthrough

Definition of done:

- repo is presentation-ready

## Step-by-step implementation order

1. scaffold folders and packages
2. create `pyproject.toml`
3. create `config.py`
4. create `db.py`
5. create CLI entrypoint
6. create FastAPI entrypoint
7. add source config YAML and schema
8. implement fetcher
9. implement normalizer
10. add content hashing and version tracking
11. implement chunker
12. implement embedder
13. implement vector store wrapper
14. implement indexing service
15. implement retriever
16. implement generation service
17. implement `ask`
18. add eval dataset
19. add eval runner
20. polish docs/tests

## Config system

Use `config.py` to define settings and defaults. Use `.env` or environment variables to override them.

Settings should include:

- DB path
- raw data dir
- normalized data dir
- Chroma path
- embedding model
- Ollama model
- chunk size
- chunk overlap
- default top-k
- log level
- request timeout

Important:

- `.env` stores values
- `config.py` loads them, validates them, and provides defaults

## Data model

### documents

One row per logical source document.

Fields:

- `doc_id`
- `source_id`
- `title`
- `url`
- `category`
- `doc_type`
- `tags_json`
- `enabled`
- `created_at`
- `updated_at`

### document_versions

One row per fetched version.

Fields:

- `version_id`
- `doc_id`
- `fetched_at`
- `http_status`
- `content_hash`
- `content_length`
- `raw_path`
- `normalized_path`
- `extraction_method`
- `changed_from_previous`
- `etag`
- `last_modified_header`

### chunks

One row per chunk version.

Fields:

- `chunk_id`
- `doc_id`
- `version_id`
- `chunk_index`
- `text`
- `token_estimate`
- `char_count`
- `metadata_json`
- `vector_store_id`
- `created_at`

### sync_runs

Fields:

- `sync_run_id`
- `started_at`
- `completed_at`
- `status`
- `scanned_count`
- `changed_count`
- `unchanged_count`
- `failed_count`
- `notes`

### eval_runs

Fields:

- `eval_run_id`
- `started_at`
- `completed_at`
- `embedding_model`
- `llm_model`
- `retriever_top_k`
- `prompt_version`
- `results_path`

## Source config

Create `sources/aws_sources.yaml` with a curated allowlist.

Each entry should include:

- `source_id`
- `title`
- `url`
- `category`
- `doc_type`
- `tags`
- `enabled`

Use around 15-30 sources total in V1.

## Starter corpus themes

Prioritize:

- Amazon Bedrock docs
- Lambda docs
- SQS docs
- API Gateway docs
- DynamoDB docs
- Well-Architected docs
- selected AWS blog posts on Bedrock, serverless, architecture, reliability

The corpus should feel coherent: an AWS architecture + Bedrock assistant.

## Chunking design

V1 recommendation:

- chunk by paragraph-aware windows
- target roughly 150-250 tokens
- configurable overlap
- preserve headings where possible

Each chunk should store metadata:

- doc ID
- version ID
- source URL
- title
- category
- doc type
- tags
- chunk index
- content hash

## Incremental sync logic

Hash normalized content, not raw HTML.

Per source:

1. fetch
2. normalize
3. compute hash
4. compare to latest version
5. if unchanged, skip indexing
6. if changed, create new version and re-index

V1 tradeoff:

- delete old vectors for a changed doc
- re-chunk and re-embed the whole document
- do not attempt chunk-level diffing yet

This is simpler and safer for a small corpus.

## Retrieval design

V1:

- dense retrieval only
- embed query locally
- retrieve top-k = 5 to 8
- optionally cap chunks per document
- return retrieved chunk metadata and scores in debug mode

Do not overcomplicate retrieval in V1.

## Generation design

Use a grounded prompt with these rules:

- answer only from provided context
- do not invent AWS facts
- say when evidence is insufficient
- cite supporting sources

Output should include:

- concise answer
- evidence section
- uncertainty note when needed

## CLI design

Use Typer.

Commands:

- `init`
- `sync`
- `refresh`
- `list-docs`
- `inspect-doc`
- `inspect-chunks`
- `retrieve`
- `ask`
- `eval run`
- `eval report`

Important:

- CLI is an interface, not where business logic lives
- CLI should call shared service modules

## API design

Use FastAPI.

Suggested endpoints:

- `GET /health`
- `POST /sync`
- `POST /refresh`
- `GET /documents`
- `GET /documents/{doc_id}`
- `GET /documents/{doc_id}/chunks`
- `POST /retrieve`
- `POST /ask`
- `POST /eval/run`

Important:

- API is also just an interface
- route handlers should call the same underlying service functions used by the CLI

## Local setup expectations

Local setup should be simple and reproducible.

Expected tools:

- Python 3.14.1+
- Ollama
- uv or pip
- SQLite

Example flow:

- install dependencies
- pull local Ollama model
- initialize project
- run sync
- run ask
- run eval

## Eval strategy

Use a lightweight but credible eval setup.

Create 25-50 questions across:

- factual lookup
- paraphrase
- synthesis across multiple docs
- ambiguous questions
- out-of-scope questions that should be declined

Track at least:

- expected source hit@k
- grounding quality
- completeness
- citation quality
- abstention correctness

Use JSONL or CSV outputs that are easy to review manually.

## Nice-to-have phase 2 features

After V1:

- hybrid retrieval
- reranking
- metadata filtering
- scheduled refresh
- lightweight frontend
- support for more doc types
- Docker packaging
- optional cloud deployment path
- chunk-level incremental indexing
- analytics/debug dashboard

## Ongoing review instruction

When reviewing code:

1. compare implementation against this plan
2. flag unnecessary complexity
3. prefer clarity over framework-heavy patterns
4. keep business logic out of CLI/API layers
5. preserve incremental-sync architecture
6. preserve local-first design
7. suggest pragmatic improvements, not theoretical rewrites

If the current implementation differs from this plan, note whether the difference is:

- acceptable simplification
- technical debt
- bug
- scope creep
- worthwhile improvement

Keep the project portfolio-friendly and interview-friendly.

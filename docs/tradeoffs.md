# Tradeoffs

Design decisions made in this project and the reasoning behind them.

## Local-first over cloud

Everything runs on a single machine — SQLite instead of Postgres, Chroma instead of Pinecone, Ollama instead of a hosted API. This keeps the project free to run, easy to set up, and independent of external accounts or API keys. The tradeoff is lower performance and model quality compared to cloud services, but for a portfolio project demonstrating pipeline design, that's the right call.

## Curated allowlist over crawling

Sources are defined in a YAML file rather than discovered by crawling. This keeps the corpus predictable and small enough to iterate on quickly. A crawler would be more realistic for production but adds complexity (robots.txt, deduplication, rate limiting, link extraction) that doesn't serve the core goal of demonstrating RAG pipeline architecture.

## Document-level re-indexing over chunk-level diffing

When a document changes, all its old vectors are deleted and the entire document is re-chunked and re-embedded. A smarter approach would diff at the chunk level — only re-embed chunks whose content actually changed. But for a small corpus (dozens of documents, hundreds of chunks), the simpler approach is fast enough and avoids the complexity of chunk identity tracking across versions.

## SQLite over a heavier database

SQLite requires zero setup, ships with Python, and handles the metadata workload fine. The schema (documents, versions, chunks) is simple enough that an ORM would add more complexity than it removes. Raw SQL with parameterized queries keeps things transparent.

## sentence-transformers over API-based embeddings

`all-MiniLM-L6-v2` runs locally, produces 384-dimensional vectors, and loads in seconds. It's not the highest quality embedding model available, but it's free, fast, and keeps the project self-contained. Swapping to a better model later is a one-line config change.

## Cosine distance over other metrics

Chroma is configured with cosine similarity. For normalized text embeddings, cosine and dot product behave similarly. Cosine is the more common default and works well with sentence-transformers models. No strong reason to use anything else here.

## Ollama over direct model loading

Using Ollama as an HTTP server rather than loading models directly via transformers or llama.cpp keeps the generation code simple (just an HTTP call) and lets the user choose their model independently. The tradeoff is requiring Ollama to be installed and running, but it's a lightweight dependency.

## Prompt-based abstention over post-processing

The system relies on prompt instructions and a minimum chunk count gate to handle abstention. A more robust approach would analyze the answer after generation — check for hedging language, compare against known patterns, or use a classifier. But prompt-based abstention is simple, works reasonably well, and avoids adding another model or processing step.

## JSONL evals over a framework

The eval system is a simple loop: run questions, score results, print a report. No eval framework (like promptfoo, ragas, or deepeval) is used. This keeps dependencies minimal and makes the eval logic fully transparent. The tradeoff is fewer built-in metrics and no fancy dashboards, but for 25-50 questions the simple approach is easier to understand and extend.

## Flat project structure over framework patterns

No dependency injection, no abstract base classes, no plugin system. Modules import each other directly. This is intentional — the codebase is small enough that direct imports are clearer than indirection. If the project grew significantly, introducing interfaces and DI would make sense, but at this scale it would be over-engineering.

## BeautifulSoup over readability-lxml or trafilatura

BeautifulSoup is simple and familiar. It does pull in some boilerplate (nav, footer) that a smarter extractor like trafilatura would skip. This is a known limitation listed in open issues. For V1, the simpler tool that works is preferable to the better tool that adds another dependency to learn and debug.

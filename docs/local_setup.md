# Local Setup

Step-by-step guide to get the project running on your machine.

## Prerequisites

- **Python 3.14.1+** — check with `python --version`
- **Ollama** — install from [ollama.com](https://ollama.com)
- **uv** (recommended) or pip — install uv from [docs.astral.sh/uv](https://docs.astral.sh/uv/)

## 1. Clone and install

```bash
git clone https://github.com/your-username/aws-docs-rag-lab.git
cd aws-docs-rag-lab
uv sync
```

If using pip instead:

```bash
pip install -e .
```

## 2. Set up Ollama

Start Ollama if it's not already running:

```bash
ollama serve
```

Pull the default model:

```bash
ollama pull mistral
```

You can use a different model by setting `OLLAMA_MODEL` in your `.env` file.

## 3. Configure

Copy the example env file:

```bash
cp .env.example .env
```

The defaults work out of the box. Key settings you might want to change:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `mistral` | Which Ollama model to use |
| `TOP_K` | `5` | Number of chunks to retrieve per query |
| `MAX_DISTANCE` | `1.0` | Cosine distance threshold for filtering weak matches |
| `CHUNK_SIZE` | `200` | Target chunk size in tokens (approximate) |
| `DEBUG` | `True` | Show retrieval details in responses |

## 4. Initialize

```bash
raglab init
```

This creates the SQLite database and data directories under `data/`.

## 5. Sync documents

```bash
raglab sync
```

Fetches all enabled sources from `sources/aws_sources.yaml`, extracts text, generates embeddings, and stores everything locally. This takes a few minutes on the first run.

Re-running `sync` is fast — only changed documents are reprocessed.

## 6. Ask a question

```bash
raglab ask "What is Amazon Bedrock?"
```

The system retrieves relevant chunks, builds a grounded prompt, and generates an answer with citations via Ollama.

## 7. Run evals

```bash
raglab eval
```

Runs all questions in `data/eval_dataset.jsonl` through the pipeline, scores the results, and prints a summary report. Results are saved to `data/eval_results/latest.jsonl`.

## Other commands

```bash
raglab healthcheck     # check system health
raglab show-config     # print current settings
raglab sources         # list configured source URLs
```

## Running the API

```bash
uvicorn app.api.main:app --reload
```

Endpoints:

- `GET /health` — health check
- `POST /query/ask` — ask a question (JSON body: `{"question": "..."}`)

## Running tests

```bash
uv run pytest tests/ -v
```

## Troubleshooting

**"Connection refused" when asking a question** — Ollama isn't running. Start it with `ollama serve`.

**"Model not found"** — You need to pull the model first: `ollama pull mistral` (or whatever model is set in `.env`).

**Sync is slow** — The first sync downloads all documents and generates embeddings. Subsequent syncs skip unchanged documents. If you're on a slower machine, the embedding step is the bottleneck.

**Empty answers or "not enough information"** — Run `raglab sync` first to populate the index. If the index is populated, try lowering `MAX_DISTANCE` threshold or increasing `TOP_K` in `.env`.


# FastAPI RAG API (ChromaDB + Ollama)

A minimal **Retrieval-Augmented Generation (RAG)** API built with **FastAPI**, **ChromaDB** (persistent local vector store), and **Ollama** for local LLM inference.

## What’s in here

- **FastAPI service** in `app.py`
  - `POST /query`: retrieves the most relevant doc from ChromaDB and asks the LLM to answer using that context
  - `POST /add`: adds new text to the knowledge base at runtime
- **Embedding pipeline** in `embed_docs.py`
  - reads all `docs/*.txt` files
  - stores them in a persistent ChromaDB collection (`./db`)
- **CI-friendly mode**
  - set `USE_MOCK_LLM=1` to skip Ollama and return retrieved context directly (see `.github/workflows/ci.yml`)

## Requirements

- **Python** 3.11+
- **Ollama** (for real LLM answers): install from `https://ollama.com/download`
- A model pulled locally (example):

```bash
ollama pull tinyllama
```

## Quickstart (local)

Install deps:

```bash
pip install fastapi uvicorn chromadb ollama
```

Embed docs into ChromaDB:

```bash
python embed_docs.py
```

Run the API:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open docs:
- Swagger UI: `http://127.0.0.1:8000/docs`

## API usage

### Query

```bash
curl -X POST "http://127.0.0.1:8000/query?q=What%20is%20Kubernetes%3F"
```

Response:

```json
{"answer":"..."}
```

### Add knowledge

```bash
curl -X POST "http://127.0.0.1:8000/add?text=Kubernetes%20is%20..."
```

## Configuration

- **`USE_MOCK_LLM`**
  - `1`: disables Ollama calls and returns the retrieved context (useful for CI)
  - `0` (default): uses Ollama to generate answers
- **`OLLAMA_HOST`**
  - Default: `http://host.docker.internal:11434`
  - Use this to point to your Ollama instance (especially in Docker/Kubernetes)

## Run with Docker

Build the image (embeddings are baked in at build time via `python embed_docs.py`):

```bash
docker build -t rag-app .
```

Run the container:

```bash
docker run -p 8000:8000 -e OLLAMA_HOST="http://host.docker.internal:11434" rag-app
```

If you see an error like “Failed to connect to Ollama”, confirm:
- Ollama is running on your host machine
- Your container can reach it via `host.docker.internal`

## Deploy to Kubernetes (local cluster)

These manifests assume a locally built image named `rag-app` (note `imagePullPolicy: Never`).

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Then access the NodePort service (port depends on your cluster). You can also port-forward:

```bash
kubectl port-forward service/rag-app-service 8000:8000
```

## Update the knowledge base

- Add/edit `.txt` files in `docs/`
- Re-run:

```bash
python embed_docs.py
```

## Project layout

- `app.py`: FastAPI app + RAG query logic
- `embed_docs.py`: embeds `docs/*.txt` into ChromaDB (`./db`)
- `docs/`: knowledge base source files
- `db/`: persistent ChromaDB data directory (created/updated locally)
- `deployment.yaml`, `service.yaml`: Kubernetes manifests

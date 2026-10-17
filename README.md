# AI Dating Profile Search

A prototype AI learning project exploring semantic search over the [59k OkCupid Dating Profiles dataset](https://huggingface.co/datasets/SpiceeChat/OkCupid-59k-Anonymized-Profiles) using vector embeddings.

The goal is to build a simple search engine that combines traditional filters with natural language queries to find relevant profiles.

> **Note:** This project uses a historical, anonymized dataset for experimentation. The profiles are not current dating prospects.

## Overview

The project uses [Sentence Transformers](https://www.sbert.net/) to generate vector embeddings and [Qdrant](https://qdrant.tech/) as the vector database for storing and searching those embeddings.

Users can search profiles using a combination of:

- **Hard filters:** Structured criteria such as age, height, location, gender, orientation, and relationship status.
- **Natural language search:** Queries describing the kind of person someone is looking for, expressed in plain English.
- **Semantic ranking:** Profiles are ranked by the semantic similarity between the query and profile information.

The objective is to build an end-to-end semantic search application, from embedding generation to a searchable web interface.

## Tech Stack

- **Python** — application logic and API
- **uv** — Python project and dependency management
- **Sentence Transformers** — text embedding generation
- **BAAI/bge-small-en-v1.5** — embedding model with 384-dimensional vectors
- **Qdrant** — vector database
- **Docker Compose** — local database infrastructure
- **FastAPI** — search API
- **HTML, CSS, JavaScript** — frontend

## How It Works

The application follows a data-processing and search pipeline:

```text
┌────────────────────────┐
│   Dating Profile Data  │
│    ~59,000 Profiles    │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│    Data Processing     │
│  Normalize & Structure │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Sentence Transformers│
│  Generate Embeddings   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│     Qdrant Database    │
│   Vectors + Metadata   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│       FastAPI           │
│  Filters + Vector Search│
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│        Web UI           │
│  Ranked Profile Results │
└────────────────────────┘
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads/) — use the version specified in `.python-version`.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package and project manager.
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine with the Docker Compose plugin.
- Git

Verify your installations:

```bash
python --version
uv --version
docker --version
docker compose version
```

### 1. Clone the Repository

```bash
git clone https://github.com/mehti-roshan/dating-search-engine
cd dating-search-engine
```

### 2. Install Dependencies

For an existing project with a committed lockfile:

```bash
uv sync
```

### 3. Configure Environment Variables

Copy the `.env.example` to `.env` file in the project root:

These are the default values used by the application.

| Variable | Description |
|---|---|
| `QDRANT_URL` | URL of the Qdrant instance |
| `COLLECTION_NAME` | Name of the Qdrant collection |
| `EMBEDDING_MODEL` | Hugging Face embedding model |
| `BATCH_SIZE` | Number of profiles processed per embedding batch |
| `VECTOR_SIZE` | Number of dimensions of vectors the model and database use |

The embedding model `BAAI/bge-small-en-v1.5` generates 384-dimensional vectors. The Qdrant collection must use the same vector size.

Do not commit `.env` to version control.

### 4. Start Qdrant with Docker Compose

Start the database from the project root:

```bash
docker compose up -d
```

Check that the container is running:

```bash
docker compose ps
```

The default Qdrant endpoints are:

- **HTTP API:** http://localhost:6333
- **Web dashboard:** http://localhost:6333/dashboard
- **gRPC:** `localhost:6334`

Verify that Qdrant is responding:

```bash
curl http://localhost:6333/healthz
```

You can also open the dashboard in your browser to inspect collections and stored points.

To view database logs:

```bash
docker compose logs -f
```

To stop the database:

```bash
docker compose down
```

Stopping the container does not normally delete persisted data. Avoid removing Docker volumes unless you intentionally want to delete the database contents.

### 5. Ingest Profiles into Qdrant

Once Qdrant is running, execute:

```bash
uv run python -m src.ingest
```

The ingestion process should:

1. Convert profile information into text suitable for semantic search.
2. Generate embeddings using `BAAI/bge-small-en-v1.5`.
3. Create or use the configured Qdrant collection.
4. Store each embedding alongside its profile payload.

The payload contains the profile metadata used to display results and apply structured filters.

**Important:** The first run downloads the embedding model if it is not already cached. This requires an internet connection and may take some time.

For approximately 59,000 profiles, ingestion can take several minutes or longer, depending on your hardware.

Wait for the script to finish successfully before starting the API.

### 6. Start the API and Web Interface

Start the FastAPI application from the project root:

```bash
uv run uvicorn src.api:app --reload
```

The `--reload` option automatically restarts the server when Python files change. It is intended for development.

Once the server starts, open:

**Web interface:** http://127.0.0.1:8000

### 7. Search Profiles

The web interface supports natural language queries and structured filters.

Example queries:

- `Someone who loves live music, indie rock, and discovering new bands`
- `A creative person who enjoys writing, art, and intellectual conversations`
- `Someone who enjoys hiking, nature, and spending weekends outdoors`
- `A person interested in technology, science, and learning new things`

Use the filters to narrow results by supported criteria, such as:

- Age range
- Location
- Gender
- Orientation
- Relationship status
- Height range

Click **Find people** to submit the query.

The frontend sends the query and selected filters to `/api/search`. The API embeds the query, searches Qdrant, applies structured filters, and returns ranked results.

The UI displays profile information and essays from the stored payload.

**Similarity scores are not compatibility percentages.** They indicate how closely a profile's embedding matches the search query according to the vector similarity metric.

## Development Commands

Run Python commands through `uv`:

```bash
# Run the ingestion script
uv run python -m src.ingest

# Start the development API server
uv run uvicorn src.main:app --reload

# Add a dependency
uv add <package-name>

# Run a Python script
uv run python path/to/script.py

# Synchronize the environment with the lockfile
uv sync

# Check whether the lockfile is up to date
uv lock --check
```

Replace the API module path if your FastAPI application lives somewhere other than `src/main.py`.

### Database Management

```bash
# Start Qdrant
docker compose up -d

# Inspect running containers
docker compose ps

# Follow Qdrant logs
docker compose logs -f

# Stop Qdrant
docker compose down
```

## Troubleshooting

### Cannot connect to Qdrant

Make sure the Docker container is running:

```bash
docker compose ps
```

Check the health endpoint:

```bash
curl http://localhost:6333/healthz
```

Verify that `.env` contains:

```env
QDRANT_URL=http://localhost:6333
```

If the API or ingestion script runs inside another Docker container, `localhost` will refer to that container rather than the Qdrant container. In that setup, use the Qdrant service name on the shared Docker network.

### No search results

Check that:

1. The ingestion script completed successfully.
2. The expected Qdrant collection exists.
3. The collection contains points.
4. The configured collection name matches the ingestion and API configuration.
5. The filters are compatible with the actual payload values.
6. The search query is not overly restrictive.

### Embedding dimension mismatch

The collection's vector size must match the model's output dimension.

For `BAAI/bge-small-en-v1.5`, use:

```python
VECTOR_SIZE = 384
```

If you change the embedding model, you may need to recreate the collection and re-ingest the dataset.

### Missing Python dependencies

Run:

```bash
uv sync
```

If you add or remove dependencies, update the project using `uv add` or `uv remove` rather than editing the environment manually.

### Frontend cannot reach the API

Check that:

- The API server is running.
- You opened the interface through the FastAPI server rather than directly opening `index.html` as a file.
- The frontend submits requests to `/api/search`.
- The API returns the expected response structure, including a `results` array.

## Current Limitations

- The dataset contains historical profiles and should not be interpreted as a list of currently active dating prospects.
- Semantic search is approximate and can misunderstand nuanced descriptions.
- Structured filters are needed for requirements that must be strictly enforced.
- Similarity scores do not represent personal compatibility.
- Search quality depends on how profile text is prepared and embedded.
- This is a learning prototype, not a production-ready dating platform.

## Future Improvements

- Improve profile text preprocessing and embedding strategies.
- Add pagination and sorting.
- Add automated tests for search filters and API behavior.
- Improve ingestion progress reporting and error handling.
- Evaluate search quality with a representative set of test queries.

## License and Dataset

This project is intended for learning and experimentation.

Dataset: [SpiceeChat/OkCupid-59k-Anonymized-Profiles on Hugging Face](https://huggingface.co/datasets/SpiceeChat/OkCupid-59k-Anonymized-Profiles)

Review the dataset's license and terms of use before redistributing the data or deploying an application based on it.
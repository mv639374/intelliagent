
-----------------------------------------------------------------------------------------------------------------------------------------------------------

# **Phase-0** (Foundation Setup)


## Step 0.1 | Initialize repository 
* Makefile
* .gitignore
* .env.example && backend/.env.example && frontend/.env.example
* README.md
* License

```bash
make help
cp .env.example .env
```

## Step 0.2 | Backend Python Environment
* backend/pyproject.toml

```bash
# Run all these from backend directory

pyenv install 3.11.9  # install
pyenv local 3.11.9    # make it local
python --version  # check version
pyenv install --list | grep 3.11  # check available python versions

# setup virtual enviroment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]" 
# or
make install-backend
# or
pip install -e .

# then run
uv run ruff check .
uv run mypy app

# verify it prints OK
uv run python -c "import fastapi, langchain, langgraph; print('OK')"
```

## Step 0.3 | Frontend Next.js Environment
`Will come back to it later`
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --eslint
npm install 
# or
make install-frontend
npm run dev
npm run build
npm run lint
```

## Step 0.4 | Docker Compose for local development
* docker-compose.yml
* docker-compose.dev.yml
* docker-compose.prod.yml
* deploy/.dockerignore
* deploy/Dockerfile.api
* deploy/Dockerfile.web
* deploy/Dockerfile.worker

### Services:
* postgres:16-alpine — port 5432, volume postgres_data
* redis:7-alpine — port 6379, volume redis_data
* elasticsearch:8.11.0 or opensearchproject/opensearch:2 — port 9200, single-node, volume es_data
* qdrant/qdrant or chromadb/chroma — port 6333/8000, volume vector_data
* api service — build ./backend, depends on db/redis/es, port 8000, env file, hot-reload volume mounts
* web service — build ./frontend, depends on api, port 3000, env file, hot-reload
* worker service — build ./workers, depends on redis, env file

```bash
# Build & Run the services
docker-compose -f docker-compose.dev.yml up -d --build
# or
make run-dev
# Start DBs (docker compose -f docker-compose.dev.yml up -d postgres redis elasticsearch)

# shows all containers healthy
docker compose -f docker-compose.dev.yml ps

# Connect to postgres: 
psql postgres://user:pass@localhost:5432/dbname

# Connect to redis (returns PONG): 
redis-cli -h localhost ping 

# Elasticsearch (returns cluster info): 
curl http://localhost:9200

# Set DOCKERHUB_USERNAME and DOCKERHUB_TOKEN as environment variables in github
```

### Some useful docker commands
```bash
# Install a library inside container
docker exec -it intelliagent-backend python3.11 -m pip install pandas

# Run a file inside docker
docker exec -it intelliagent-backend sh -c "cd /app && PYTHONPATH=/app python abc/xyz.py"

# Run Tests
docker compose -f docker-compose.dev.yml exec backend python -m pytest tests/ -v
# or a particular test
docker compose -f docker-compose.dev.yml exec backend python -m pytest tests/test.py

### Remove unused images
docker image prune -a

### Remove build cache (if needed)
docker builder prune -a

### Remove everything and start fresh
docker system prune -a --volumes
```

## Step 0.5 | CI/CD pipeline skeleton
* .github/workflows/ ci.yml cd.yml lint.yml test.yml
* .pre-commit-config.yaml
* scripts/healthcheck.sh

### CI jobs
* Lint backend (ruff, mypy)
* Lint frontend (eslint, tsc)
* Run backend unit tests (pytest)
* Run frontend unit tests (jest/vitest)
* Build Docker images (api, web, worker)

```bash
# Install the tool (from root project folder): 
pip install pre-commit

# Set up the git hooks: 
pre-commit install

# Then every time before git commit
pre-commit run --all-files

# Exits 0 when services are up
chmod +x scripts/healthcheck.sh
./scripts/healthcheck.sh
```

## Step 0.6 | Documentation Scaffolding
* docs/architecture.md — High-level architecture, component diagram
* docs/development-guide.md — Setup, workflows, standards
* docs/rag-design.md — RAG pipeline design (to be detailed in Phase 1)
* docs/mcp-integration.md — MCP design (to be detailed in Phase 2)
* docs/security-policies.md — Security model (to be detailed in Phase 3)
* docs/ops-runbook.md — Operations guide (to be detailed in Phase 4)
* docs/api-specification.md — Placeholder for OpenAPI spec


-----------------------------------------------------------------------------------------------------------------------------------------------------------



# **Phase-1** (Core RAG & Data Pipelines)

* Now everything will be in the backend directory

* Document Ingestion
* OCR
* Chunking
* Embedding
* Indexing
* Hybrid Retrieval (keyword: elasticsearch; vector: qdrant)

## Step 1.1 | Database Schema & Models

* alembic.ini (update after initialiing alembic)
* alembic/env.py (update after initialiing alembic)
* app/db/session.py    (This file creates the async session factory that our application will use to interact with the database.)
* app/db/base.py
* app/db/base_class.py
* app/models/user.py
* app/models/project.py
* app/models/document.py
* app/models/chunk.py
* app/models/conversation.py
* app/models/message.py
* app/models/audit.py
* scripts/manual_db_test.py


```bash
# Run from ./backend/ directory
alembic init alembic

# Generate the migration file and Apply the migration
docker exec -it intelliagent-backend bash -c "cd /app && alembic revision --autogenerate -m 'initial_schema' && alembic upgrade head"

# Restart backend
docker compose -f docker-compose.dev.yml restart backend
#or only build backend again
docker compose -f docker-compose.dev.yml up --build -d backend

# Check all tables in db
docker exec -it intelliagent-db psql -U user -d intelliagent_db
# then '\dt' for tables and '\dt documents' for particular table

# It should return OK
uv run python -c "from app.models import User, Document, Chunk; print('OK')"

# Or if you want to drop everything in the database
docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
rm -rf backend/alembic/versions/*.py

# Delete all documents & chunks
docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "DELETE FROM chunks; DELETE FROM documents;"
```


## Step 1.2 | Document Ingestion Pipeline

* spaCy model needed for PII redaction

* app/rag/ingest/base_connector.py      (This is the abstract base class that all our connectors will inherit from.)
* app/rag/ingest/file_connector.py      (Handles local file uploads from the API.)
* app/rag/ingest/s3_connector.py        (A basic connector for fetching documents from an S3 bucket.)
* app/rag/ingest/drive_connector.py     (A placeholder for the Google Drive connector.)
* app/rag/ingest/preprocessor.py        (Cleans and normalizes raw text content.)
* app/rag/ingest/pii_redactor.py        (Detects and redacts Personally Identifiable Information (PII).)
* app/rag/ingest/metadata_extractor.py  (Extracts metadata like author and title from files.)
* workers/tasks/ingest_tasks.py         (This is the Celery task that orchestrates the entire ingestion process asynchronously.)
* app/api/v1/documents.py               (The FastAPI endpoint for uploading documents.)

* workers/celery_app.py                 (This file defines the Celery application instance, configuring it to use Redis as the broker.)
* app/settings.py                       (This file uses Pydantic to manage application settings and load them from environment variables.)
* app/main.py                           (This is the main entry point for the FastAPI application.)
* app/dependencies.py                   (A place for common, project-wide dependencies. For now, it will just re-export the database session getter.)
* app/exceptions.py                     (A place for custom exception handlers. (Empty for now).)
* app/middleware.py                     (A place for custom middleware. (Empty for now).)
* app/api/v1/router.py                  (This router combines all the individual API endpoints for the v1 version of our API.)
* app/api/deps.py                       (This file will contain dependencies specific to the API, like user authentication. For now, we will create stubs.)
* tests/rag/ingest/test_file_connector.py

```bash
# Start the celery worker (run from root, then upload a pdf at POST upload endpoint):
docker compose -f docker-compose.dev.yml exec backend celery -A workers.celery_app worker --loglevel=info
# or 
docker compose -f docker-compose.dev.yml exec backend celery -A workers.celery_app worker -l info --pool=solo

# then check the database table
docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT filename, status FROM documents;"
```


## Step 1.3 | OCR Integration





























-----------------------------------------------------------------------------------------------------------------------------------------------------------

# **Phase 2** (Agentic Orchestration)

* Build LangGraph multi-agent graphs with task-specific agents, tool calling, memory, interrupts, and streaming

## Step-2.1 | LangGraph Foundation

* app/models/graph_checkpoint.py         (defines the graph_checkpoints table schema using SQLAlchemy.)
* app/agents/config.py                   (This file centralizes configuration for our agents, allowing us to easily switch between LLM providers based on your priority .)
* app/agents/state.py                    (This defines the AgentState, the shared memory structure that is passed between all nodes in our graph.)
* app/agents/checkpointer.py             (This class implements LangGraph's persistence layer, saving and loading the state from our Postgres database.)
* app/agents/interrupts.py               (This file contains the logic for pausing the graph to wait for human approval.)
* app/agents/graph_factory.py            (This is a placeholder for the graph builder. For this step, it will create a simple two-node graph to pass the checkpoint tests.)
* app/db/base.py                         (update: import this new model so alembic can discover it)
* scripts/agent_foundation_test.py       (to validate the foundation.)
* tests/agents/test_graph_factory.py     (building the simple graph and asserting that the expected placeholder nodes ("start" and "end") exist in the compiled graph structure.)

## Step-2.2 | Agent Nodes Implementation

* app/agents/nodes/base_node.py     (This abstract base class provides a consistent structure for all our agent nodes.)
* app/agents/nodes/planner.py       (This node is responsible for breaking down the user's query into a sequence of actionable steps. )
* app/agents/nodes/retriever.py     (This node uses the powerful hybrid RAG retriever we built in Phase 1 to fetch relevant context from our knowledge base.)
* app/agents/nodes/solver.py        (The Solver's job is to synthesize the retrieved context into a coherent answer, complete with citations.)
* app/agents/nodes/verifier.py      (The Verifier acts as a quality control gate, ensuring the generated answer is grounded in the provided context by checking for citations.)
* app/agents/nodes/tool_node.py     (This node is a placeholder for executing tool calls. It simulates finding a tool call and appending a mock result to the context.)

* tests/agents/nodes/test_planner.py
* tests/agents/nodes/test_retriever.py
* tests/agents/nodes/test_solver.py
* tests/agents/nodes/test_verifier.py
* tests/agents/nodes/test_tool_node.py
* scripts/node_checkpoint_test.py

## Step-2.3 | Conditional Edges & Routing

* app/agents/edges/routing_logic.py
* app/agents/edges/conditional_edges.py
* tests/agents/test_agent_execution.py
* app/agents/state.py                     (update)
* app/agents/graph_factory.py             (update)

## Phase 2.4 | Memory & Context Management

* app/agents/state.py   (update)
* app/agents/memory/postgres_store.py
* app/agents/memory/redis_store.py
* app/agents/memory/memory_management.py
* tests/agents/memory/test_memory_manager.py
* scripts/memory_checkpoint_test.py

# Step 2.5 | Streaming & Real-time Updates

* app/agents/graph_factory.py                    (update file: We need to add a new node to the beginning of our graph that loads the conversation history into the state. This makes the agent aware of the conversation's context before it starts planning.)
* app/api/v1/chat.py                             (This file is updated with a new /stream endpoint that uses FastAPI's StreamingResponse to stream events directly from the LangGraph astream_events method.)
* frontend/src/app/page.tsx                      (display the stream)
* frontend/src/components/chat/ChatStream.tsx    (This is the main chat component that handles user input, initiates the stream, and renders the conversation.)
* tests/api/v1/test_streaming.py

# Step 2.6
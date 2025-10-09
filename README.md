# IntelliAgent

_Enterprise-Grade Agentic AI Platform - More details coming soon._

- Stop the containers: docker-compose -f docker-compose.dev.yml down
- Stop & delete the containers: docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
- Rebuild the containers: docker-compose -f docker-compose.dev.yml build --no-cache
- Start the containers: docker-compose -f docker-compose.dev.yml up -d --build

Steps:

1. Run from ./backend/
   `uv pip install -e ".[dev]"`

2. Run from the project root ./
   `pre-commit install`

Delete all documents:
`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "DELETE FROM chunks; DELETE FROM documents;"`

# Rebuild container with new dependencies

`docker compose -f docker-compose.dev.yml up --build -d backend`

# Run tests

`docker compose -f docker-compose.dev.yml exec backend python -m pytest tests/ -v`

---

# Start celery worker:

`docker compose -f docker-compose.dev.yml exec backend celery -A workers.celery_app worker -l info --pool=solo`

# 1. Check chunks table for PII redaction and metadata:

`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT text, chunk_metadata FROM chunks WHERE document_id = (SELECT id FROM documents WHERE filename = 'pii_sample.pdf');"`

# 2. Check chunks table for tables:

`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT text FROM chunks WHERE document_id = (SELECT id FROM documents WHERE filename = 'table_sample.pdf') AND text LIKE 'Table:%';"`

# 3. Check documents table for status INDEXED:

`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT filename, status FROM documents;"`

# IntelliAgent

_Enterprise-Grade Agentic AI Platform - More details coming soon._

---



# 1. Check chunks table for PII redaction and metadata:

`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT text, chunk_metadata FROM chunks WHERE document_id = (SELECT id FROM documents WHERE filename = 'pii_sample.pdf');"`

# 2. Check chunks table for tables:

`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT text FROM chunks WHERE document_id = (SELECT id FROM documents WHERE filename = 'table_sample.pdf') AND text LIKE 'Table:%';"`

# 3. Check documents table for status INDEXED:

`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT filename, status FROM documents;"`


# Get whole list of users
`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "SELECT id, username, email, role, created_at FROM users;"`
# Delete all of them
`docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "TRUNCATE TABLE users CASCADE;"`

# IntelliAgent Architecture Overview

This document outlines the high-level architecture of the IntelliAgent platform.

## 1. System Context Diagram (C4 Model)

The diagram below shows the system's context, illustrating how it interacts with users and external systems.

```mermaid
graph TD
    subgraph IntelliAgent_Platform [IntelliAgent Platform]
        direction LR
        A[Frontend Web UI]
        B[Backend API]
        C[Multi-Agent System]
        D[RAG Pipeline]
        E[/"Postgres, Redis, Elasticsearch, Qdrant"/]
    end

    User[Knowledge Worker] -->|Interacts via Browser| A
    A -->|Makes API calls| B
    B -->|Orchestrates| C
    C -->|Uses Tools| D
    C -->|Accesses| ExternalSystems[External Enterprise Systems (GitHub, Google Drive, Slack)]
    D -->|Ingests/Retrieves Data| E

    style User fill:#08427b,stroke:#08427b,color:#fff
    style ExternalSystems fill:#999,stroke:#999,color:#fff
```

## 2. Component Overview

- **Frontend Web UI**: A Next.js application providing the user interface for chat, document management, and administration.
- **Backend API**: A FastAPI service that handles business logic, user authentication, and orchestrates agentic workflows.
- **Multi-Agent System**: Powered by LangGraph, this component manages complex, stateful workflows by coordinating specialized agents.
- **RAG Pipeline**: The Retrieval-Augmented Generation system responsible for ingesting, chunking, embedding, and retrieving information from various data sources.
- **Data Stores**: A collection of databases for structured data (PostgreSQL), caching (Redis), keyword search (Elasticsearch), and vector storage (Qdrant).
- **External Systems**: Enterprise systems that IntelliAgent connects to via the Managed Connection Platform (MCP) to perform actions on behalf of the user.

## 3. Data Flow

1. **Ingestion**: Documents are uploaded via the UI, sent to the API, and processed by an asynchronous RAG ingestion pipeline. They are chunked, embedded, and stored in Elasticsearch and Qdrant.
2. **Query**: A user sends a query through the UI. The Backend API routes this to the Multi-Agent System.
3. **Execution**: An agent uses the RAG pipeline to retrieve relevant context. It may also use tools to interact with external systems.
4. **Response**: The agent synthesizes the retrieved context and tool outputs into a final answer, which is streamed back to the user through the API and displayed in the UI.

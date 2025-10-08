# IntelliAgent

_Enterprise-Grade Agentic AI Platform - More details coming soon._

- Stop the containers: docker stop $(docker ps -aq)
- Stop & delete the containers: docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
- Start the containers: docker-compose -f docker-compose.dev.yml up -d --build

Steps:

1. Run from ./backend/
   `uv pip install -e ".[dev]"`

2. Run from the project root ./
   `pre-commit install`

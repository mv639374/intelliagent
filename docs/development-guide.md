# IntelliAgent Development Guide

This guide details how to set up the local development environment, our coding standards, and the Git workflow.

## 1. Local Development Setup

### Prerequisites

- Git
- Docker & Docker Compose
- `make`
- Python 3.11+ (managed via `pyenv` recommended)
- Node.js 20+ (managed via `nvm` recommended)
- `uv` (Python package manager): `pip install uv`
- `pre-commit`: `pip install pre-commit`

### Step-by-Step Instructions

1.  **Clone the Repository**:

    ```bash
    git clone [https://github.com/your-username/intelliagent.git](https://github.com/your-username/intelliagent.git)
    cd intelliagent
    ```

2.  **Configure Environment Variables**:
    Copy the root environment template and fill in the required values.

    ```bash
    cp .env.example .env
    ```

3.  **Install Dependencies**:
    The `Makefile` simplifies dependency installation for both frontend and backend.

    ```bash
    make setup
    ```

4.  **Install Git Hooks**:
    This enables automatic code formatting and linting before each commit.

    ```bash
    pre-commit install
    ```

5.  **Start the Services**:
    Use the `Makefile` to launch all services with Docker Compose.
    ```bash
    make run-dev
    ```
    You can check the status of the containers with `docker ps`.

## 2. Coding Standards

- **Backend (Python)**:
  - Follow PEP 8 guidelines.
  - Use `ruff` for linting and formatting (configured in `.pre-commit-config.yaml` and `pyproject.toml`).
  - Use `mypy` for static type checking. All functions must have type hints.
  - Write docstrings for all modules, classes, and functions.
- **Frontend (TypeScript/React)**:
  - Use ESLint and Prettier for linting and formatting (configured in `.eslintrc.json` and `.prettierrc`).
  - Follow the rules defined in the project's ESLint configuration.

## 3. Git Workflow

1.  Create a new feature branch from `main`: `git checkout -b feat/my-new-feature`.
2.  Make your changes and commit them. Pre-commit hooks will run automatically.
3.  Push your branch to the remote repository.
4.  Open a Pull Request (PR) against the `main` branch.
5.  The CI pipeline will automatically run linting, tests, and build checks.
6.  At least one peer review is required before merging.

```

```

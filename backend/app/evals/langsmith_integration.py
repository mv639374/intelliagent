from langsmith import Client
from app.settings import settings

def get_langsmith_client():
    """Initializes and returns the LangSmith client if configured."""
    if settings.LANGSMITH_API_KEY:
        return Client(api_key=settings.LANGSMITH_API_KEY)
    return None

def log_eval_to_langsmith(dataset_name: str, results: dict):
    """Logs the summary of an evaluation run to LangSmith."""
    client = get_langsmith_client()
    if not client:
        print("LangSmith client not configured. Skipping logging.")
        return
    
    try:
        client.create_run(
            name=f"RAG Eval - {dataset_name}",
            run_type="chain",  # CHANGED: "test" → "chain"
            project_name=settings.LANGCHAIN_PROJECT,
            inputs={"dataset": dataset_name},
            outputs=results
        )
        print("Logged evaluation summary to LangSmith.")
    except Exception as e:
        print(f"Failed to log to LangSmith: {e}")

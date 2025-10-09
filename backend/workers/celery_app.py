import multiprocessing as mp

mp.set_start_method("spawn", force=True)


import os

from celery import Celery

# Get the Redis URL from an environment variable, with a default for local dev
REDIS_URL = os.getenv("REDIS_URL", "redis://intelliagent-redis:6379/0")

# Create the Celery app instance
celery_app = Celery(
    "workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["workers.tasks.ingest_tasks"],  # List of modules to import when the worker starts
)

# Configure Celery
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

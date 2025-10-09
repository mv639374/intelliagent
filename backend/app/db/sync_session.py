# backend/app/db/sync_session.py
"""
Synchronous database session for Celery workers.
Celery tasks should NEVER use AsyncSessionLocal - it causes event loop conflicts.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.settings import settings

# Convert async DATABASE_URL to sync
SYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://")

# Create synchronous engine for Celery tasks
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Synchronous session factory
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)


@contextmanager
def get_sync_db():
    """
    Context manager for synchronous database sessions in Celery tasks.

    Usage:
        with get_sync_db() as db:
            result = db.execute(select(User))
            db.commit()
    """
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

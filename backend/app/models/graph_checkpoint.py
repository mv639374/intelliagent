import uuid
from sqlalchemy import Column, LargeBinary, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base_class import Base

class GraphCheckpoint(Base):
    __tablename__ = 'graph_checkpoints'

    thread_id = Column(String, primary_key=True)
    checkpoint = Column(LargeBinary, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), primary_key=True)
import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base_class import Base

class EvaluationRun(Base):
    __tablename__ = 'evaluation_runs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_name = Column(String, nullable=False)
    metrics = Column(JSONB, nullable=False) # e.g., {"precision@5": 0.8, "recall@10": 0.7}
    created_at = Column(DateTime, default=func.now())
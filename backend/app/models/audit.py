import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.base_class import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Can be null for system actions
    action = Column(String, nullable=False)
    resource_type = Column(String)  # e.g., 'document', 'project'
    resource_id = Column(String)
    details = Column(JSONB)
    timestamp = Column(DateTime, default=func.now())

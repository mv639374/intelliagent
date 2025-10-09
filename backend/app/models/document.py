# import uuid
# from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Enum as SQLAlchemyEnum
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from app.db.base_class import Base

# class DocumentStatus(str, SQLAlchemyEnum):
#     PENDING = "pending"
#     PROCESSING = "processing"
#     INDEXED = "indexed"
#     FAILED = "failed"

# class Document(Base):
#     __tablename__ = 'documents'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
#     filename = Column(String, nullable=False)
#     mime_type = Column(String)
#     size_bytes = Column(Integer)
#     sha256 = Column(String(64), unique=True, nullable=False)
#     status = Column(SQLAlchemyEnum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
#     owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
#     created_at = Column(DateTime, default=func.now())

#     owner = relationship("User", back_populates="documents")
#     project = relationship("Project", back_populates="documents")
#     chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")


import enum
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    mime_type = Column(String)
    size_bytes = Column(Integer)
    sha256 = Column(String(64), unique=True, nullable=False)
    status = Column(SQLAlchemyEnum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    owner = relationship("User", back_populates="documents")
    project = relationship("Project", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

# import uuid
# from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID, JSONB
# from app.db.base_class import Base

# class Chunk(Base):
#     __tablename__ = 'chunks'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id'), nullable=False)
#     chunk_index = Column(Integer, nullable=False)
#     text = Column(Text, nullable=False)
#     vector_id = Column(String, unique=True) # This can be a UUID or another string format from the vector DB
#     metadata = Column(JSONB)
#     created_at = Column(DateTime, default=func.now())

#     document = relationship("Document", back_populates="chunks")


import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    vector_id = Column(String, unique=True)  # This can be a UUID or another string format from the vector DB
    chunk_metadata = Column(JSONB)  # Renamed from 'metadata' to avoid SQLAlchemy reserved word
    created_at = Column(DateTime, default=func.now())

    document = relationship("Document", back_populates="chunks")

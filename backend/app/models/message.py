# import uuid
# from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text, Enum as SQLAlchemyEnum
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID, JSONB
# from app.db.base_class import Base

# class MessageRole(str, SQLAlchemyEnum):
#     USER = "user"
#     ASSISTANT = "assistant"

# class Message(Base):
#     __tablename__ = 'messages'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
#     role = Column(SQLAlchemyEnum(MessageRole), nullable=False)
#     content = Column(Text, nullable=False)
#     citations = Column(JSONB) # Store list of cited document/chunk IDs
#     created_at = Column(DateTime, default=func.now())

#     conversation = relationship("Conversation", back_populates="messages")


import enum
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Text, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(SQLAlchemyEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    citations = Column(JSONB)  # Store list of cited document/chunk IDs
    created_at = Column(DateTime, default=func.now())

    conversation = relationship("Conversation", back_populates="messages")

# import uuid
# from sqlalchemy import Column, String, DateTime, func, Enum as SQLAlchemyEnum
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from app.db.base_class import Base

# class UserRole(str, SQLAlchemyEnum):
#     ADMIN = "admin"
#     USER = "user"

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     username = Column(String, unique=True, index=True, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#     projects = relationship("Project", back_populates="owner")
#     documents = relationship("Document", back_populates="owner")


import enum
import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    projects = relationship("Project", back_populates="owner")
    documents = relationship("Document", back_populates="owner")

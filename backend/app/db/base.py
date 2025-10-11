# Import the Base from its single source of truth
from app.db.base_class import Base

# Import all of your models so that they are registered with the Base's metadata.
# This is crucial for Alembic's autogenerate feature to work correctly.
from app.models.user import User
from app.models.project import Project
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.audit import AuditLog
from app.models.evaluation import EvaluationRun
from app.models.graph_checkpoint import GraphCheckpoint

# You can optionally create an __all__ here if you want, but it's not necessary for Alembic.
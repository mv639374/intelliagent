# import pickle
# from typing import Any, Optional, List
# from langgraph.checkpoint import BaseCheckpointSaver
# from langgraph.checkpoint.base import Checkpoint, CheckpointTuple
# from app.db.sync_session import get_sync_db
# from app.models.graph_checkpoint import GraphCheckpoint
# from sqlalchemy import select, delete

# class PostgresCheckpointer(BaseCheckpointSaver):
#     """
#     A checkpointer that stores agent graph state in a PostgreSQL database.
#     """
#     def __init__(self):
#         super().__init__()

#     async def aget_tuple(self, config: dict) -> Optional[CheckpointTuple]:
#         thread_id = config["configurable"]["thread_id"]
#         with get_sync_db() as db:
#             stmt = select(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id)
#             saved = db.execute(stmt).scalar_one_or_none()
#             if not saved:
#                 return None
            
#             return CheckpointTuple(
#                 config=config,
#                 checkpoint=pickle.loads(saved.checkpoint),
#                 parent_config=None,
#             )

#     def list(self, config: dict) -> List[CheckpointTuple]:
#         # Not strictly needed for our current use case, but required by the interface.
#         return []

#     async def aput(self, config: dict, checkpoint: Checkpoint) -> dict:
#         thread_id = config["configurable"]["thread_id"]
#         with get_sync_db() as db:
#             # Delete existing checkpoint for the thread
#             db.execute(delete(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id))
            
#             # Create a new one
#             new_checkpoint = GraphCheckpoint(
#                 thread_id=thread_id,
#                 checkpoint=pickle.dumps(checkpoint),
#             )
#             db.add(new_checkpoint)
#             db.commit()
#         return config













import pickle
from typing import Any, Optional, List
from langgraph.checkpoint import BaseCheckpointSaver
from langgraph.checkpoint.base import Checkpoint, CheckpointTuple
from app.db.sync_session import get_sync_db
from app.models.graph_checkpoint import GraphCheckpoint
from sqlalchemy import select, delete

class PostgresCheckpointer(BaseCheckpointSaver):
    """
    A checkpointer that stores agent graph state in a PostgreSQL database.
    """
    def __init__(self):
        super().__init__()

    def get_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        thread_id = config["configurable"]["thread_id"]
        with get_sync_db() as db:
            stmt = select(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id)
            saved = db.execute(stmt).scalar_one_or_none()
            if not saved:
                return None
            
            return CheckpointTuple(
                config=config,
                checkpoint=pickle.loads(saved.checkpoint),
                metadata={},
                parent_config=None,
            )

    def list(self, config: dict) -> List[CheckpointTuple]:
        # Not strictly needed for our current use case, but required by the interface.
        return []

    def put(self, config: dict, checkpoint: Checkpoint, metadata: dict) -> dict:
        thread_id = config["configurable"]["thread_id"]
        with get_sync_db() as db:
            # Delete existing checkpoint for the thread
            db.execute(delete(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id))
            
            # Create a new one
            new_checkpoint = GraphCheckpoint(
                thread_id=thread_id,
                checkpoint=pickle.dumps(checkpoint),
            )
            db.add(new_checkpoint)
            db.commit()
        return config

    def put_writes(self, config: dict, writes: list, task_id: str) -> None:
        """Store intermediate writes linked to a checkpoint."""
        # For simple implementation, can be a no-op or store in separate table
        pass  # Or implement if you need to track intermediate writes














import pickle
from typing import Any, Optional, List
from langgraph.checkpoint import BaseCheckpointSaver
from langgraph.checkpoint.base import Checkpoint, CheckpointTuple
from app.db.sync_session import get_sync_db
from app.models.graph_checkpoint import GraphCheckpoint
from sqlalchemy import select, delete


class PostgresCheckpointer(BaseCheckpointSaver):
    """
    A checkpointer that stores agent graph state in a PostgreSQL database.
    """

    def __init__(self):
        super().__init__()

    def get_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        thread_id = config["configurable"]["thread_id"]
        with get_sync_db() as db:
            stmt = select(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id)
            saved = db.execute(stmt).scalar_one_or_none()
            if not saved:
                return None
            return CheckpointTuple(
                config=config,
                checkpoint=pickle.loads(saved.checkpoint),
                metadata={},
                parent_config=None,
            )

    async def aget_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        """Async version of get_tuple for async graph execution."""
        thread_id = config["configurable"]["thread_id"]
        with get_sync_db() as db:
            stmt = select(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id)
            saved = db.execute(stmt).scalar_one_or_none()
            if not saved:
                return None
            return CheckpointTuple(
                config=config,
                checkpoint=pickle.loads(saved.checkpoint),
                metadata={},
                parent_config=None,
            )

    def list(self, config: dict) -> List[CheckpointTuple]:
        # Not strictly needed for our current use case, but required by the interface.
        return []

    def put(self, config: dict, checkpoint: Checkpoint, metadata: dict) -> dict:
        thread_id = config["configurable"]["thread_id"]
        with get_sync_db() as db:
            # Delete existing checkpoint for the thread
            db.execute(delete(GraphCheckpoint).where(GraphCheckpoint.thread_id == thread_id))
            # Create a new one
            new_checkpoint = GraphCheckpoint(
                thread_id=thread_id,
                checkpoint=pickle.dumps(checkpoint),
            )
            db.add(new_checkpoint)
            db.commit()
        return config

    def put_writes(self, config: dict, writes: list, task_id: str) -> None:
        """Store intermediate writes linked to a checkpoint."""
        # For simple implementation, can be a no-op or store in separate table
        pass  # Or implement if you need to track intermediate writes

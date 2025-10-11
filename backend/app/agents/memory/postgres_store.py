from typing import List, Dict, Any
from sqlalchemy import select
from app.db.sync_session import get_sync_db
from app.models.message import Message, MessageRole

class PostgresMemoryStore:
    """Handles long-term storage of conversation messages in PostgreSQL."""

    def save_message(self, conversation_id: str, role: str, content: str):
        """Saves a single message to the messages table."""
        with get_sync_db() as db:
            message = Message(
                conversation_id=conversation_id,
                role=MessageRole(role),
                content=content
            )
            db.add(message)
            db.commit()

    def load_history(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Loads the last N messages for a conversation from PostgreSQL."""
        with get_sync_db() as db:
            stmt = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            results = db.execute(stmt).scalars().all()
            # Reverse to maintain chronological order (oldest first)
            return [
                {"role": msg.role.value, "content": msg.content}
                for msg in reversed(results)
            ]

postgres_store = PostgresMemoryStore()
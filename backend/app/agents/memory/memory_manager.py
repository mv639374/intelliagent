from typing import List, Dict, Any
from .redis_store import redis_store
from .postgres_store import postgres_store

class MemoryManager:
    """
    Orchestrates loading and saving conversation history, using Redis as a
    cache and PostgreSQL as the persistent store.
    """
    async def load_history(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Loads conversation history. Tries Redis first, falls back to PostgreSQL.
        """
        # 1. Try to load from Redis cache
        history = redis_store.load_history(conversation_id, limit)
        if history:
            print(f"--- ⚡️ Memory: Cache hit for conversation {conversation_id[:8]} ---")
            return history
            
        # 2. If cache miss, load from PostgreSQL
        print(f"--- 💾 Memory: Cache miss. Loading from Postgres for conversation {conversation_id[:8]} ---")
        history = postgres_store.load_history(conversation_id, limit)
        
        # 3. Populate the cache for subsequent requests
        if history:
            for message in history:
                redis_store.save_message(conversation_id, message["role"], message["content"])
        
        return history

    async def save_message(self, conversation_id: str, role: str, content: str):
        """
        Saves a message to both the long-term store (Postgres) and the
        short-term cache (Redis).
        """
        print(f"--- 💾 Memory: Saving message to Postgres and Redis for conversation {conversation_id[:8]} ---")
        postgres_store.save_message(conversation_id, role, content)
        redis_store.save_message(conversation_id, role, content)

memory_manager = MemoryManager()
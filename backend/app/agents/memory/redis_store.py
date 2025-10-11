import json
from typing import List, Dict, Any
import redis
from app.settings import settings

class RedisMemoryStore:
    """Handles short-term caching of conversation messages in Redis."""

    def __init__(self, ttl: int = 3600): # Cache for 1 hour
        self.client = redis.from_url(settings.REDIS_URL)
        self.ttl = ttl

    def _get_key(self, conversation_id: str) -> str:
        return f"conv:{conversation_id}:messages"

    def load_history(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Loads the last N messages for a conversation from the Redis cache."""
        key = self._get_key(conversation_id)
        # Fetch the last `limit` items from the list
        messages_json = self.client.lrange(key, -limit, -1)
        if not messages_json:
            return []
        return [json.loads(msg) for msg in messages_json]

    def save_message(self, conversation_id: str, role: str, content: str):
        """Saves a message to the Redis cache and trims the history."""
        key = self._get_key(conversation_id)
        message = {"role": role, "content": content}
        
        # Use a pipeline for atomic operations
        pipe = self.client.pipeline()
        pipe.rpush(key, json.dumps(message))
        pipe.ltrim(key, -20, -1) # Keep only the last 20 messages in the cache
        pipe.expire(key, self.ttl)
        pipe.execute()

redis_store = RedisMemoryStore()
import asyncio
import uuid
import redis
from app.agents.memory.memory_manager import memory_manager
from app.settings import settings
from app.db.sync_session import get_sync_db

# Import from app.models to load all models at once
from app.models import *


def clear_redis_cache(conv_id: str):
    """Clear Redis cache for a conversation."""
    client = redis.from_url(settings.REDIS_URL)
    key = f"conv:{conv_id}:messages"
    client.delete(key)
    print(f"Cleared Redis cache for {conv_id[:8]}")


def create_test_user_and_conversation(conv_id: str):
    """Create a test user and conversation in the database."""
    with get_sync_db() as db:
        # Create test user with all required fields
        user = User(
            id=uuid.uuid4(),
            email=f"test_{uuid.uuid4().hex[:8]}@example.com",
            username=f"test_user_{uuid.uuid4().hex[:6]}",
            hashed_password="dummy_test_hash"  # Required field
        )
        db.add(user)
        db.flush()
        
        # Create conversation with valid user_id
        conversation = Conversation(
            id=conv_id,
            user_id=user.id
        )
        db.add(conversation)
        db.commit()
    print(f"Created user and conversation {conv_id[:8]}")


async def run_memory_tests():
    """Runs integration checks for the MemoryManager."""
    conv_id = str(uuid.uuid4())
    
    create_test_user_and_conversation(conv_id)
    clear_redis_cache(conv_id)
    
    print("\n--- Running Memory Checkpoint Tests ---\n")

    # Checkpoint 1: Store 3 messages
    try:
        await memory_manager.save_message(conv_id, "user", "Message 1")
        await memory_manager.save_message(conv_id, "assistant", "Message 2")  # Changed from "ai"
        await memory_manager.save_message(conv_id, "user", "Message 3")
        history = await memory_manager.load_history(conv_id)
        assert len(history) == 3, f"Expected 3 messages, got {len(history)}"
        print("✅ 1. Store conversation (3 messages): PASSED")
    except Exception as e:
        print(f"❌ 1. Store conversation: FAILED - {e}")

    # Checkpoint 2: Trimming
    try:
        await memory_manager.save_message(conv_id, "user", "Message 4")
        history = await memory_manager.load_history(conv_id, limit=3)
        assert len(history) == 3, f"Expected 3 messages, got {len(history)}"
        assert history[0]["content"] == "Message 2", f"Expected 'Message 2', got {history[0]['content']}"
        print("✅ 2. Trimming (limit=3): PASSED")
    except Exception as e:
        print(f"❌ 2. Trimming: FAILED - {e}")

    # Checkpoint 3: Load from cache
    try:
        history_cached = await memory_manager.load_history(conv_id, limit=3)
        assert len(history_cached) == 3, f"Expected 3 messages, got {len(history_cached)}"
        print("✅ 3. Load from cache: PASSED")
    except Exception as e:
        print(f"❌ 3. Load from cache: FAILED - {e}")

    # Checkpoint 4: Verify Redis cache
    try:
        client = redis.from_url(settings.REDIS_URL)
        key = f"conv:{conv_id}:messages"
        cached = client.lrange(key, 0, -1)
        assert len(cached) > 0
        print("✅ 4. Redis cache hit: PASSED")
    except Exception as e:
        print(f"❌ 4. Redis cache hit: FAILED - {e}")

    print("\n--- Memory Checkpoint Tests Complete ---\n")


if __name__ == "__main__":
    asyncio.run(run_memory_tests())

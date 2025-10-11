import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from app.agents.memory.memory_manager import MemoryManager

@pytest.mark.asyncio
@patch('app.agents.memory.memory_manager.redis_store', new_callable=MagicMock)
@patch('app.agents.memory.memory_manager.postgres_store', new_callable=MagicMock)
async def test_memory_manager_cache_hit(mock_postgres_store, mock_redis_store):
    """Tests that the manager returns data from Redis when it's a cache hit."""
    # 1. Setup
    conv_id = "test_conv_1"
    mock_redis_store.load_history.return_value = [{"role": "user", "content": "Hello from Redis"}]
    
    manager = MemoryManager()
    
    # 2. Action
    history = await manager.load_history(conv_id)
    
    # 3. Assertions
    mock_redis_store.load_history.assert_called_once_with(conv_id, 10)
    mock_postgres_store.load_history.assert_not_called()
    assert len(history) == 1
    assert history[0]["content"] == "Hello from Redis"

@pytest.mark.asyncio
@patch('app.agents.memory.memory_manager.redis_store', new_callable=MagicMock)
@patch('app.agents.memory.memory_manager.postgres_store', new_callable=MagicMock)
async def test_memory_manager_cache_miss(mock_postgres_store, mock_redis_store):
    """Tests that the manager falls back to Postgres on a cache miss and populates the cache."""
    # 1. Setup
    conv_id = "test_conv_2"
    mock_redis_store.load_history.return_value = [] # Simulate cache miss
    mock_postgres_store.load_history.return_value = [{"role": "user", "content": "Hello from Postgres"}]
    
    manager = MemoryManager()
    
    # 2. Action
    history = await manager.load_history(conv_id)
    
    # 3. Assertions
    mock_redis_store.load_history.assert_called_once_with(conv_id, 10)
    mock_postgres_store.load_history.assert_called_once_with(conv_id, 10)
    # Verify that the cache is populated after the miss
    mock_redis_store.save_message.assert_called_once_with(conv_id, "user", "Hello from Postgres")
    assert len(history) == 1
    assert history[0]["content"] == "Hello from Postgres"

@pytest.mark.asyncio
@patch('app.agents.memory.memory_manager.redis_store', new_callable=MagicMock)
@patch('app.agents.memory.memory_manager.postgres_store', new_callable=MagicMock)
async def test_memory_manager_save_message(mock_postgres_store, mock_redis_store):
    """Tests that saving a message calls both the cache and the persistent store."""
    # 1. Setup
    conv_id = "test_conv_3"
    manager = MemoryManager()
    
    # 2. Action
    await manager.save_message(conv_id, "ai", "Response")
    
    # 3. Assertions
    mock_postgres_store.save_message.assert_called_once_with(conv_id, "ai", "Response")
    mock_redis_store.save_message.assert_called_once_with(conv_id, "ai", "Response")
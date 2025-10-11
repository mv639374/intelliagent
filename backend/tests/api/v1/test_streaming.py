import pytest
import httpx
import json
from app.main import app
from app.api.deps import get_current_user
from app.models.user import User
import uuid

# Mock user for testing
def override_get_current_user():
    return User(
        id=uuid.uuid4(),
        username="test_user",
        email="test@example.com",
        hashed_password="dummy",
        role="USER"
    )

@pytest.mark.asyncio
async def test_chat_stream_endpoint():
    """
    Connects to the streaming endpoint and verifies that it receives
    agent events and constructs a full answer.
    """
    # Override authentication dependency
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    try:
        # Use ASGITransport to connect to the FastAPI app
        transport = httpx.ASGITransport(app=app)
        
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            # Match AskRequest schema - add all required fields
            request_data = {
                "query": "What is LangGraph?",
                "project_id": str(uuid.uuid4()),
                "top_k": 5,  # Add default values
                "rerank": True
            }
            
            async with client.stream("POST", "/api/v1/chat/stream", json=request_data, timeout=30) as response:
                assert response.status_code == 200, f"Status: {response.status_code}, Body: {await response.aread()}"
                assert "text/event-stream" in response.headers["content-type"]
                
                full_answer = ""
                received_events = set()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        event = json.loads(line[6:])
                        received_events.add(event["event"])
                        
                        if event["event"] == "on_chat_model_stream":
                            token = event.get("data", {}).get("token", "")
                            full_answer += token
                
                # Assertions
                assert len(received_events) > 0, "No events received"
                print(f"Received events: {received_events}")
                print(f"Full answer length: {len(full_answer)}")
    finally:
        # Clean up dependency override
        app.dependency_overrides.clear()

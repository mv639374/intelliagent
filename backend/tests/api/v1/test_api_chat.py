# backend/tests/api/v1/test_api_chat.py

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import create_access_token, get_password_hash
from app.models.user import User, UserRole
from app.models.project import Project
import uuid

@pytest.mark.asyncio
async def test_ask_endpoint(client: AsyncClient, db: AsyncSession):
    # 1. Setup: Create a user and project with unique email
    user_id = uuid.uuid4()
    project_id = uuid.uuid4()
    unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"  # Generate unique email
    
    test_user = User(
        id=user_id,
        username=f"testuser_{uuid.uuid4().hex[:8]}",
        email=unique_email,
        hashed_password=get_password_hash("password"),
        role=UserRole.USER,
    )
    test_project = Project(id=project_id, name="Chat Project", owner_id=user_id)
    db.add(test_user)
    db.add(test_project)
    await db.commit()

    # 2. Get JWT Token
    token = create_access_token(data={"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 3. (Assume document is already indexed) Make a valid request
    response = await client.post(
        "/api/v1/chat/ask",
        headers=headers,
        json={"query": "What is LangGraph?", "project_id": str(project_id)},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is LangGraph?"
    assert "citations" in data
    assert len(data["citations"]) > 0

    # 4. Test Authentication Error
    response_no_auth = await client.post(
        "/api/v1/chat/ask",
        json={"query": "test", "project_id": str(project_id)},
    )
    assert response_no_auth.status_code in [401, 403]

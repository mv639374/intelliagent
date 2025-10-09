from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.project import Project
from app.models.user import User

# --- TODO: These are stubs and will be replaced by a full OAuth2 implementation in Phase 3 ---


async def get_current_user(db: AsyncSession = Depends(get_db)) -> User:
    """
    Stub dependency to get the 'current user'.
    For now, it just fetches the first user from the database.
    """
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Test user not found. Please seed the DB.")
    return user


async def get_current_project(db: AsyncSession = Depends(get_db)) -> Project:
    """
    Stub dependency to get the 'current project'.
    For now, it just fetches the first project from the database.
    """
    result = await db.execute(select(Project).limit(1))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Test project not found. Please seed the DB.")
    return project

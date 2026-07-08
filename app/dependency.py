from app.core.database import SessionLocal#core/database.py bata SessionLocal import gareko ho, jasko kaam database session create garne ho

from sqlalchemy.ext.asyncio import AsyncSession#sQLAlchemy ko AsyncSession import gareko ho, jasko kaam asynchronous database session handle garne ho
from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:#database session generator function that yields an asynchronous database session for use in FastAPI endpoints
    async with SessionLocal() as session:#SessionLocal() is called to create a new asynchronous database session. The async with statement ensures that the session is properly closed after use, even if an error occurs during the execution of the code block.
        yield session#s
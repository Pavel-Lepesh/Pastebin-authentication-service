from sqlalchemy.ext.asyncio import AsyncSession
from app.backend_db.db import async_session_maker


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

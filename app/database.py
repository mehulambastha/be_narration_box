from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://narrationbox:nb123@localhost:5432/nb_task_manager")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

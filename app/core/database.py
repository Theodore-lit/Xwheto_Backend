"""Configuration SQLAlchemy asynchrone (AsyncIO + asyncpg)."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Base déclaratif pour tous les modèles
Base = declarative_base()

# Engine asynchrone
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Vérifie que la connexion est vive avant utilisation
)

# Session factory asynchrone
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dépendance FastAPI pour obtenir une session DB.

    Yields:
        AsyncSession: Session SQLAlchemy asynchrone

    Example:
        @app.get("/users/")
        async def list_users(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(User))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialise la base de données (crée les tables si elles n'existent pas).

    À utiliser en développement seulement. En production, utiliser Alembic.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Ferme l'engine et toutes les connexions ouvertes."""
    await engine.dispose()

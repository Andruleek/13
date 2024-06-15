from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import contextlib
from src.conf.config import create_async_engine, async_sessionmaker, SQLALCHEMY_DATABASE_URL

# Створити синхронний двигун SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Створення синхронного виробника сеансів
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Оголошення базового класу для моделей SQLAlchemy
Base = declarative_base()

# Створення асинхронного класу менеджера сеансів
class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Сеанс не ініціалізовано")

        async with self._session_maker() as session:
            try:
                yield session
            except Exception as err:
                print(err)
                await session.rollback()
            finally:
                await session.close()

# Створіть менеджер сеансів для нашої бази даних використання URL-адреси конфігурації
sessionmanager = DatabaseSessionManager(SQLALCHEMY_DATABASE_URL)

# Функція для отримання асинхронного сеансу бази даних
async def get_db():
    async with sessionmanager.session() as session:
        yield session
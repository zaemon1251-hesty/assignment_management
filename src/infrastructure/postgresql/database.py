from typing import Iterator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
import os

engine = create_engine(
    os.getenv('DATABASE_URL'),
    encoding="utf-8",
    echo=True  # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    # class_=AsyncSession
)


Base = declarative_base()


# async def get_session() -> Iterator[Session]:
#     async with SessionLocal() as session:
#         yield session

def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

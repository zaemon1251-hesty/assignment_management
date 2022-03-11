from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
import os
from src.domain.user import AuthedUser, User
from src.infrastructure.postgresql.users.UserOrm import UserOrm
from sqlalchemy.orm.exc import NoResultFound
from src.infrastructure.cert.auth import AuthDriverImpl

engine = create_engine(
    os.getenv('DATABASE_URL'),
    encoding="utf-8",
    echo=True  # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


async def make_superuser():
    su = AuthedUser(
        name="admin",
        email=os.getenv("GMAIL_ACCOUNT"),
        hash_password=AuthDriverImpl.get_password_hash(os.getenv("GMAIL_PASSWORD")))
    sessions = get_session()
    session = sessions.__next__()
    session.begin()
    try:
        session.query(UserOrm).filter_by(name=su.name).one()
    except NoResultFound:
        session.add(UserOrm.from_domain(su))
        session.commit()

if __name__ == "__main__":
    create_tables()
    make_superuser()

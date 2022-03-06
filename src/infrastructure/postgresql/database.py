from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


engine = create_engine(
    os.getenv('DATABASE_URL'),
    encoding="utf-8",
    echo=True  # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)


Base = declarative_base()
Base.query = session.query_property()


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()

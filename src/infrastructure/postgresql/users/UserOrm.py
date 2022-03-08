from datetime import datetime, timezone
from typing import Optional
from src.domain.user import User
from src.infrastructure.postgresql.database import Base
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class UserOrm(Base):
    """
    User (model)
    params:
    id->int
    name->string
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(2000), nullable=False)
    moodle_id = Column(String(30))
    moodle_password = Column(String(30))
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)
    submissions = relationship("submission", backref="users")

    @classmethod
    def to_domain(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            moodle_id=self.email,
            moodle_password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_domain(data: User) -> "UserOrm":
        now = datetime.utcnow()
        return UserOrm(
            id=data.id,
            name=data.name,
            email=data.email,
            password=data.password,
            moodle_id=data.email,
            moodle_password=data.password,
            created_at=now,
            updated_at=now
        )

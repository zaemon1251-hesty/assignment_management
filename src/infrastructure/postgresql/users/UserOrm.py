from datetime import datetime, timezone
from typing import Optional
from src.domain.user import User, AuthedUser
from src.infrastructure.postgresql.database import Base
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
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
    name = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    hash_password = Column(String(2000), nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)

    @classmethod
    def to_domain(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            disabled=self.disabled,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def to__authed(self) -> AuthedUser:
        return AuthedUser(
            id=self.id,
            name=self.name,
            email=self.email,
            disabled=self.disabled,
            hash_password=self.hash_password,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_domain(data: AuthedUser) -> "UserOrm":
        now = datetime.utcnow()
        return UserOrm(
            id=data.id,
            name=data.name,
            email=data.email,
            hash_password=data.hash_password,
            created_at=now,
            updated_at=now
        )

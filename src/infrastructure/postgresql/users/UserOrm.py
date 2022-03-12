from datetime import datetime, timezone
from typing import Optional, Union
from domain.user import User, AuthedUser
from infrastructure.postgresql.database import Base
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
    id: Union[int, Column] = Column(
        Integer, primary_key=True, autoincrement=True)
    name: Union[str, Column] = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    hash_password = Column(String(2000), nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)

    def to_domain(self,) -> User:
        return User.from_orm(self)

    def to__authed(self) -> AuthedUser:
        return AuthedUser.from_orm(self)

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

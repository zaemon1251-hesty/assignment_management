from abc import ABC, abstractclassmethod, abstractmethod
from ctypes import Union
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.domain.user import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Optional[User]
    exp: float


class AuthDriver(ABC):
    """driver (interface of the authorizing process)"""

    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> Token:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_token(self, token: str) -> User:
        raise NotImplementedError

    @abstractclassmethod
    def get_password_hash(cls, password: str) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def authenticate_token(
            cls,
            token: str) -> TokenData:
        raise NotImplementedError

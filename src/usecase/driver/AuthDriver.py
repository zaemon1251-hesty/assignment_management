from abc import ABC, abstractclassmethod, abstractmethod
from src.domain.user import User, AuthedUser
from src.usecase.token import Token, TokenData


class AuthDriver(ABC):
    """driver (interface of the authorizing process)"""

    @abstractmethod
    async def create_access_token(self, email: str, password: str) -> Token:
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

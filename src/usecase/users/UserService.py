from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.user import User
from .UserModel import UserQueryModel


class UserService(ABC):
    @abstractmethod
    async def fetch_all(self, query: UserQueryModel) -> List[User]:
        raise NotImplementedError

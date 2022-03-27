from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.domain.user import User


class UserQueryModel(BaseModel):
    id: Optional[List[int]] = None
    name: Optional[List[str]] = None
    email: Optional[List[str]] = None
    disabled: Optional[bool] = None
    created_at: Optional[List[datetime]] = None
    updated_at: Optional[List[datetime]] = None
    created_be: Optional[datetime] = None
    created_af: Optional[datetime] = None
    updated_be: Optional[datetime] = None
    updated_af: Optional[datetime] = None


class UserService(ABC):
    @abstractmethod
    async def fetch_all(self, query: UserQueryModel) -> List[User]:
        raise NotImplementedError

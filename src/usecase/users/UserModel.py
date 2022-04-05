from datetime import datetime
from typing import Callable, List, Optional
from pydantic import BaseModel, Field
from src.domain.user import User, AuthedUser


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


class UserCommandModel(BaseModel):
    name: Optional[str] = Field(default=None, example="zaemon1251")
    email: Optional[str] = Field(default=None, example="test@example.com")
    disabled: Optional[bool] = Field(default=False)
    password: Optional[str] = None

    def to_authed(
            self,
            func: Callable[[str], str],
            password: str) -> AuthedUser:
        return AuthedUser(
            # id=self.id,
            name=self.name,
            email=self.email,
            disabled=self.disabled,
            # created_at=self.created_at,
            # updated_at=self.updated_at,
            hash_password=func(password)
        )

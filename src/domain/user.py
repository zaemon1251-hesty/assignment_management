from datetime import datetime
from typing import Optional

from src.domain.base import OrmBase


class User(OrmBase):
    """User represents your collection of user as an entity."""

    name: str
    email: str
    disabled: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AuthedUser(User):
    hash_password: str

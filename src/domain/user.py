from datetime import datetime
from typing import Optional

from src.domain import OrmBase


class User(OrmBase):
    """User represents your collection of user as an entity."""

    id: int
    name: str
    email: str
    moodle_id: Optional[str] = None
    moodle_password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AuthedUser(User):
    token: str
    hash_password: str

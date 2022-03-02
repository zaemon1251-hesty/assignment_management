from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional


class User(BaseModel):
    """User represents your collection of user as an entity."""

    id: int
    name: str
    email: str
    password: str
    moodle_user_id: Optional[str] = None
    moodle_user_password: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    class Config:
        orm_mode = True

from pydantic.dataclasses import dataclass
from typing import Optional


@dataclass(init=False, eq=True, frozen=True)
class User:
    """User represents your collection of user as an entity."""

    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        password: str,
        moodle_user_id: Optional[str] = None,
        moodle_user_password: Optional[str] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: int = id
        self.name: str = name
        self.email: str = email
        self.password: str = password
        self.moodle_user_id: str = moodle_user_id
        self.moodle_user_password: str = moodle_user_password
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

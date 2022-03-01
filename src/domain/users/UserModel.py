from dataclasses import dataclass
from typing import Optional


@dataclass(init=False, eq=True, frozen=True)
class User:
    """course represents your collection of course as an entity."""

    def __init__(
        self,
        id: str,
        name: str,
        moodle_user_id: str,
        moodle_user_password: str,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.name: str = name
        self.moodle_user_id: str = moodle_user_id
        self.moodle_user_password: str = moodle_user_password
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

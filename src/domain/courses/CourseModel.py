from dataclasses import dataclass
from typing import Optional


@dataclass(init=False, eq=True, frozen=True)
class Course:
    """course represents your collection of course as an entity."""

    def __init__(
        self,
        id: str,
        title: str,
        url: str,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.title: str = title
        self.url: int = url
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

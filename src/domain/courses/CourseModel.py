from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional


class Course(BaseModel):
    """course represents your collection of course as an entity."""

    id: int
    title: str
    url: str
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    class Config:
        orm_mode = True
        validate_assignment = True

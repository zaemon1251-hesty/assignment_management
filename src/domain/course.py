from datetime import datetime
from typing import Optional

from src.domain.base import OrmBase


class Course(OrmBase):
    """course represents your collection of course as an entity."""

    title: str
    url: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

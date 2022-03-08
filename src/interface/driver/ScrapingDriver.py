from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from src.domain.assignment import Assignment
from src.domain.course import Course


class ScrapeDriver(ABC):
    """ driver (interface of web scraper html parser) """

    @abstractmethod
    async def run(moodle_id: str, moodle_password: str, keywords: List[str]) -> Tuple[List[Assignment], List[Course]]:
        raise NotImplementedError

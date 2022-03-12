from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from src.domain import (
    Assignment,
    Course
)


class ScrapeDriver(ABC):
    """ driver (interface of web scraper html parser) """

    @abstractmethod
    async def run(self, keywords: List[str]) -> Tuple[List[Assignment], List[Course]]:
        raise NotImplementedError

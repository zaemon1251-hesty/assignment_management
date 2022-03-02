from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class crude_course:
    course_title: str
    course_url: str


class crude_assignment:
    course_id: int
    assignment_title: str
    info: Optional[str]
    url: str


class FetchDriver(ABC):
    """ driver (web scraper html parser) """

    @ abstractmethod
    async def run(moodle_id: str, moodle_password: str, keywords: List[str]) -> Tuple[List[crude_assignment], List[crude_course]]:
        raise NotImplementedError

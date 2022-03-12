from src.domain.assignment import Assignment
from src.domain.course import Course
from src.infrastructure.crawl.scraping import ScrapeDriverImpl


class ScrapeDriverImplTest:
    def __init__(self):
        self.driver = ScrapeDriverImpl()

    async def test_run(self):
        res = await self.driver.run(["2021"])
        assignments, courses = res

        assert len(assignments) != 0
        assert len(courses) != 0

        assert isinstance(assignments[0], Assignment)
        assert isinstance(courses[0], Course)

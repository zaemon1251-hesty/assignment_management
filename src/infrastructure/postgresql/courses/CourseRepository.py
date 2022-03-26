from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from src.domain.CourseRepository import CourseRepository
from src.domain.course import Course
from src.infrastructure.postgresql.courses.CourseOrm import CourseOrm
from src.usecase.courses.CourseUseCase import CourseUseCaseUnitOfWork


class CourseUseCaseUnitOfWorkImpl(CourseUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        course_repository: CourseRepository,
    ):
        self.session: Session = session
        self.course_repository: CourseRepository = course_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class CourseRepositoryImpl(CourseRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch(self, id: int) -> Optional[Course]:
        try:
            Course_orm = self.session.query(
                CourseOrm).filter_by(id=id).one()
            return Course_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_by_title(self, title: str) -> Optional[Course]:
        try:
            Course_orm = self.session.query(
                CourseOrm).filter_by(title=title).one()
            return Course_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_all(self, domain: Optional[Course]) -> List[Course]:
        targets = dict(domain) if domain is not None else {}
        try:
            q = self.session.query(CourseOrm)
            for attr, value in targets.items():
                if attr == "id":
                    continue
                q = q.filter(getattr(CourseOrm, attr) == value)
            q = q.order_by(CourseOrm.updated_at)
            Course_orms = q.all()
            return list(
                map(
                    lambda Course_orm: Course_orm.to_domain(),
                    Course_orms
                )
            ) if len(Course_orms) > 0 else []
        except Exception:
            raise

    async def add(self, domain: Course) -> Course:
        try:
            Course_orm = CourseOrm.from_domain(domain)
            self.session.add(Course_orm)
            return Course_orm.to_domain()
        except Exception:
            raise

    async def update(self, domain: Course) -> Course:
        try:
            Course_orm = CourseOrm.from_domain(domain)
            target = self.session.query(
                CourseOrm).filter_by(id=domain.id).one()
            updatables = [
                "title",
                "url",
                "updated_at"
            ]
            for attr in updatables:
                value = getattr(Course_orm, attr)
                if value is not None and value != "":
                    setattr(target, attr, value)
            return target.to_domain()
        except Exception:
            raise

    async def delete(self, id: int) -> bool:
        try:
            self.session.query(CourseOrm).filter_by(id=id).delete()
            return True
        except Exception:
            raise

from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from src.domain.AssignmentRepository import AssignmentRepository
from src.domain.assignment import Assignment
from src.domain.course import Course
from src.domain.assignment import ASSIGNMENT_STATE, Assignment
from src.infrastructure.postgresql.assignments.AssignmentOrm import AssignmentOrm
from src.usecase.assignments.AssignmentUseCase import AssignmentUseCaseUnitOfWork


class AssignmentUseCaseUnitOfWorkImpl(AssignmentUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        book_repository: AssignmentRepository,
    ):
        self.session: Session = session
        self.book_repository: AssignmentRepository = book_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class AssignmentRepositoryImpl(AssignmentRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch(self, id: int) -> Optional[Assignment]:
        try:
            Assignment_orm = self.session.query(
                AssignmentOrm).filter_by(id=id).one()
            return Assignment_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_by_title(self, title: str) -> Optional[Assignment]:
        try:
            Assignment_orm = self.session.query(
                AssignmentOrm).filter_by(title=title).one()
            return Assignment_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_all(self, domain: Optional[Assignment]) -> List[Assignment]:
        targets = dict(domain)
        try:
            q = self.session.query(AssignmentOrm)
            for attr, value in targets.items():
                q = q.filter(getattr(AssignmentOrm, attr) == value)
            q = q.order_by(AssignmentOrm.updated_at)
            Assignment_orms = q.all()
            return list(
                map(
                    lambda Assignment_orm: Assignment_orm.to_domain(),
                    Assignment_orms
                )
            ) if len(Assignment_orms) > 0 else []
        except Exception:
            raise

    async def create(self, domain: Assignment) -> Assignment:
        try:
            Assignment_orm = AssignmentOrm.from_domain(domain)
            self.session.add(Assignment_orm)
            return Assignment_orm.to_domain()
        except Exception:
            raise

    async def update(self, domain: Assignment) -> Assignment:
        try:
            Assignment_orm = AssignmentOrm.from_domain(domain)
            target = self.session.query(
                AssignmentOrm).filter_by(id=domain.id).one()
            updatables = [
                "title",
                "state",
                "update_at"
            ]
            for attr in updatables:
                value = getattr(Assignment_orm, attr)
                if isinstance(value, ASSIGNMENT_STATE):
                    value = value.value
                if value is not None and value != "":
                    setattr(target, attr, value)
            return target.to_domain()
        except Exception:
            raise

    async def delete(self, id: int) -> bool:
        try:
            self.session.query(AssignmentOrm).filter_by(id=id).delete()
            return True
        except Exception:
            raise

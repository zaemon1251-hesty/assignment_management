from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from src.domain.SubmissionRepository import SubmissionRepository
from src.domain.assignment import Assignment
from src.domain.submission import SUBMISSION_STATE, Submission
from src.infrastructure.postgresql.submissions import SubmissionOrm
from src.usecase.submissions import SubmissionUseCaseUnitOfWork


class SubmissionUseCaseUnitOfWorkImpl(SubmissionUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        submission_repository: SubmissionRepository,
    ):
        self.session: Session = session
        self.submission_repository: SubmissionRepository = submission_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SubmissionRepositoryImpl(SubmissionRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch(self, id: int) -> Optional[Submission]:
        try:
            Submission_orm = self.session.query(
                SubmissionOrm).filter_by(id=id).one()
            return Submission_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_all(self, domain: Optional[Submission]) -> List[Submission]:
        targets = dict(domain) if domain is not None else {}
        try:
            ignore_params = {
                "id",
                "user",
                "assignment"
            }
            q = self.session.query(SubmissionOrm)
            for attr, value in targets.items():
                if attr in ignore_params:
                    continue
                q = q.filter(getattr(SubmissionOrm, attr) == value)
            q = q.order_by(SubmissionOrm.updated_at)
            Submission_orms = q.all()
            return list(
                map(
                    lambda Submission_orm: Submission_orm.to_domain(),
                    Submission_orms
                )
            ) if len(Submission_orms) > 0 else []
        except Exception:
            raise

    async def add(self, domain: Submission) -> Submission:
        try:
            Submission_orm = SubmissionOrm.from_domain(domain)
            self.session.add(Submission_orm)
            return Submission_orm.to_domain()
        except Exception:
            raise

    async def update(self, domain: Submission) -> Submission:
        try:
            Submission_orm = SubmissionOrm.from_domain(domain)
            target = self.session.query(
                SubmissionOrm).filter_by(id=domain.id).one()
            updatables = [
                "title",
                "state",
                "user_id",
                "assignment_id",
                "updated_at"
            ]
            for attr in updatables:
                value = getattr(Submission_orm, attr)
                if isinstance(value, SUBMISSION_STATE):
                    value = value.value
                if value is not None and value != "":
                    setattr(target, attr, value)
            return target.to_domain()
        except Exception:
            raise

    async def delete(self, id: int) -> bool:
        try:
            self.session.query(SubmissionOrm).filter_by(id=id).delete()
            return True
        except Exception:
            raise

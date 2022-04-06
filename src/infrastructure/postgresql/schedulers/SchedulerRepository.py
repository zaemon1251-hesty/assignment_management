from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from src.domain.SchedulerRepository import SchedulerRepository
from src.domain.scheduler import Scheduler
from src.infrastructure.postgresql.schedulers.SchedulerOrm import SchedulerOrm
from src.usecase.schedulers import SchedulerUseCaseUnitOfWork
from src.domain import SubmissionRepository, UserRepository


class SchedulerUseCaseUnitOfWorkImpl(SchedulerUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        scheduler_repository: SchedulerRepository,
        submission_repository: SubmissionRepository,
        user_repository: UserRepository
    ):
        self.session: Session = session
        self.scheduler_repository: SchedulerRepository = scheduler_repository
        self.submission_repository: SubmissionRepository = submission_repository
        self.user_repository: UserRepository = user_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SchedulerRepositoryImpl(SchedulerRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch(self, id: int) -> Optional[Scheduler]:
        try:
            Scheduler_orm = self.session.query(
                SchedulerOrm).filter_by(id=id).one()
            return Scheduler_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_by_title(self, title: str) -> Optional[Scheduler]:
        try:
            Scheduler_orm = self.session.query(
                SchedulerOrm).filter_by(title=title).one()
            return Scheduler_orm.to_domain()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_all(self, domain: Optional[Scheduler]) -> List[Scheduler]:
        targets = dict(domain) if domain is not None else {}
        try:
            q = self.session.query(SchedulerOrm)
            for attr, value in targets.items():
                if attr == "id":
                    continue
                q = q.filter(getattr(SchedulerOrm, attr) == value)
            q = q.order_by(SchedulerOrm.updated_at)
            Scheduler_orms = q.all()
            return list(
                map(
                    lambda Scheduler_orm: Scheduler_orm.to_domain(),
                    Scheduler_orms
                )
            ) if len(Scheduler_orms) > 0 else []
        except Exception:
            raise

    async def add(self, domain: Scheduler) -> Scheduler:
        try:
            Scheduler_orm = SchedulerOrm.from_domain(domain)
            self.session.add(Scheduler_orm)
            return Scheduler_orm.to_domain()
        except Exception:
            raise

    async def update(self, domain: Scheduler) -> Scheduler:
        try:
            Scheduler_orm = SchedulerOrm.from_domain(domain)
            target = self.session.query(
                SchedulerOrm).filter_by(id=domain.id).one()
            updatables = [
                "submission_id",
                "remind_at",
                "reminded",
                "updated_at"
            ]
            for attr in updatables:
                value = getattr(Scheduler_orm, attr)
                if value is not None and value != "":
                    setattr(target, attr, value)
            return target.to_domain()
        except Exception:
            raise

    async def delete(self, id: int) -> bool:
        try:
            self.session.query(SchedulerOrm).filter_by(id=id).delete()
            return True
        except Exception:
            raise

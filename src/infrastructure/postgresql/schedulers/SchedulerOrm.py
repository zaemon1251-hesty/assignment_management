from pydantic.dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from infrastructure.postgresql.database import Base
from domain.scheduler import Scheduler
from domain.submission import Submission
from datetime import timezone, datetime


class SchedulerOrm(Base):
    __tablename__ = 'shedulers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reminded = Column(Boolean, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)
    submission_id = Column(
        Integer,
        ForeignKey(
            'submissions.id',
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False
    )

    def to_domain(self) -> Scheduler:
        """almost same as Domain.from_orm() """
        _submission = Submission.from_orm(self.submission)
        return Scheduler(
            id=self.id,
            reminded=self.reminded,
            remind_at=self.remind_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
            submission=_submission
        )

    @staticmethod
    def from_domain(data: Scheduler) -> "SchedulerOrm":
        now = datetime.utcnow()
        return SchedulerOrm(
            id=data.id,
            reminded=data.reminded,
            remind_at=data.remind_at,
            created_at=now,
            updated_at=now,
            submission_id=data.submission.id,
        )

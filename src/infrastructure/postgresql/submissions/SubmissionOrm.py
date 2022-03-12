from datetime import datetime
from datetime import timezone
from typing import Optional
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.postgresql.database import Base
from src.domain.assignment import Assignment
from src.domain.user import User
from src.domain.submission import Submission, SUBMISSION_STATE
from src.domain.user import User


class SubmissionOrm(Base):
    """
    Submissions (model)
    params:
    id->int
    user_id->int
    assignment_id->int
    state->int
    """
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        ForeignKey(
            'users.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    assignment_id = Column(
        ForeignKey(
            'assignments.id',
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False
    )
    state = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)

    def to_domain(self) -> Submission:
        """almost same as Domain.from_orm() """
        _user = User.from_orm(self.user)
        _assignment = Assignment.from_orm(self.assignment)
        return Submission(
            id=self.id,
            user=_user,
            assignment=_assignment,
            state=SUBMISSION_STATE(self.state),
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def from_domain(data: Submission) -> "SubmissionOrm":
        now = datetime.utcnow()
        return SubmissionOrm(
            id=data.id,
            user_id=data.user.id,
            assignment_id=data.assignment.id,
            state=int(data.state),
            created_at=now,
            updated_at=now,
        )

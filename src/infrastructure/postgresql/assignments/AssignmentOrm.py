from datetime import datetime, timezone
from distutils.log import info
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.domain.assignment import Assignment, ASSIGNMENT_STATE
from infrastructure.postgresql.database import Base
from src.domain.course import Course


class AssignmentOrm(Base):
    """
    Assignments (model)
    params:
    id->int
    title->string
    status->string
    info->string

    "info" is supposed to convert to "end_at"(datetime)
    """
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    state = Column(Integer, nullable=False)
    info = Column(String(1000))
    url = Column(String(200))
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship(
        "SubmissionOrm",
        backref="assignments",
        lazy="joined"
    )

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)

    def to_domain(self) -> Assignment:
        """almost same as Domain.from_orm() """
        _course = Assignment.from_orm(self.assignment)
        return Assignment(
            id=self.id,
            course=_course,
            title=self.title,
            info=self.info,
            url=self.url,
            state=ASSIGNMENT_STATE(self.state),
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_domain(data: Assignment) -> "AssignmentOrm":
        now = datetime.utcnow()
        return AssignmentOrm(
            id=data.id,
            course_id=data.course.id,
            title=data.title,
            info=data.info,
            url=data.url,
            state=int(data.state),
            created_at=now,
            updated_at=now,
        )

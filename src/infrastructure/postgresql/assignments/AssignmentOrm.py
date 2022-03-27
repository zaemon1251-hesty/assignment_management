from datetime import datetime, timezone
from distutils.log import info
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.domain.assignment import Assignment, ASSIGNMENT_STATE
from src.infrastructure.postgresql.database import Base
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
    end_at = Column(DateTime, default=None)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship(
        "CourseOrm",
        backref="assignments",
        lazy="joined",
        foreign_keys=[course_id]
    )
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)

    def __repr__(self) -> str:
        return "<Assignment: {}>".format(self.id)

    def to_domain(self) -> Assignment:
        """almost same as Domain.from_orm() """
        return Assignment.from_orm(self)

    @staticmethod
    def from_domain(data: Assignment) -> "AssignmentOrm":
        now = datetime.utcnow()
        return AssignmentOrm(
            id=data.id,
            course_id=data.course_id,
            title=data.title,
            info=data.info,
            url=data.url,
            state=int(data.state),
            created_at=now,
            updated_at=now,
        )

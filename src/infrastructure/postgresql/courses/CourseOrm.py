from datetime import datetime, timezone
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.domain.course import Course
from src.infrastructure.postgresql.database import Base


class CourseOrm(Base):
    """
    Courses (model)
    params:
    id->int
    title->string
    """
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    url = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)

    assignments = relationship("AssignmentOrm", backref="courses")

    def to_domain(self) -> Course:
        return Course(
            id=self.id,
            title=self.title,
            url=self.url,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_domain(data: Course) -> "CourseOrm":
        now = datetime.utcnow()
        return CourseOrm(
            id=data.id,
            title=data.title,
            url=data.url,
            created_at=now,
            updated_at=now
        )

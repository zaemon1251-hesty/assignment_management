from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
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

    def __repr__(self) -> str:
        return "<Course: {}>".format(self.id)

    def to_domain(self) -> Course:
        return Course.from_orm(self)

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

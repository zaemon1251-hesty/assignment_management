import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
try:
    from setting import Base
    from setting import ENGINE
except:
    from .setting import Base
    from .setting import ENGINE

class Users(Base):
    """
    User (model)
    params:
    id->int
    name->string
    """
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    name = Column('name', String(200), nullable=False)
    moodle_userid = Column('moodle_userid', String(30))
    moodle_passwd = Column('moodle_passwd', String(30))
    assignments = relationship("UserAssignment", backref="users")
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Courses(Base):
    """
    Courses (model)
    params:
    id->int
    title->string
    """
    __tablename__ = 'courses'
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    url = Column('url', String(200))
    assignments = relationship("Assignments", backref="courses")
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Assignments(Base):
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
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    state = Column('state', Integer, nullable = False)
    info = Column('info', String(1000))
    url = Column('url', String(200))
    course_id =  Column('course_id', Integer, ForeignKey('courses.id',onupdate='CASCADE', ondelete='CASCADE'))
    assignments = relationship("UserAssignment", backref="assignments")
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserAssignment(Base):
    """
    UserAssignment (model)
    params:
    id->int
    user_id->int
    assignment_id->int
    state->int
    """
    __tablename__ = 'userassignment'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    user_id = Column('user_id', ForeignKey('users.id',onupdate='CASCADE', ondelete='CASCADE'))
    assignment_id = Column('assignment_id', ForeignKey('assignments.id',onupdate='CASCADE', ondelete='CASCADE'))
    state = Column('state', Integer, nullable = False)
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    
def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)
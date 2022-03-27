import os
from sqlalchemy.orm.exc import NoResultFound
import sys
sys.path.append("/var/www")

# こうしないと、自動整形のせいで sys.path.append よりも先に src.~ 群のインポートが始まってしまう
if True:
    from src.infrastructure.postgresql.users import UserOrm
    from src.infrastructure.postgresql.database import get_session, Base, engine
    from src.infrastructure.cert import AuthDriverImpl
    from src.domain import AuthedUser


def make_superuser():
    su = AuthedUser(
        name="admin",
        email=os.getenv("GMAIL_ACCOUNT"),
        hash_password=AuthDriverImpl.get_password_hash(os.getenv("GMAIL_PASSWORD")))
    sessions = get_session()
    session = sessions.__next__()
    session.begin()
    try:
        session.query(UserOrm).filter_by(name=su.name).one()
    except NoResultFound:
        session.add(UserOrm.from_domain(su))
        session.commit()


def create_tables():
    Base.metadata.create_all(bind=engine)


def exec_pdo():
    q = """
SELECT submissions.id AS submissions_id, submissions.user_id AS submissions_user_id, submissions.assignment_id AS submissions_assignment_id, submissions.state AS submissions_state, submissions.created_at AS submissions_created_at, submissions.updated_at AS submissions_updated_at, courses_1.id AS courses_1_id, courses_1.title AS courses_1_title, courses_1.url AS courses_1_url, courses_1.created_at AS courses_1_created_at, courses_1.updated_at AS courses_1_updated_at, assignments_1.id AS assignments_1_id, assignments_1.title AS assignments_1_title, assignments_1.state AS assignments_1_state, assignments_1.info AS assignments_1_info, assignments_1.url AS assignments_1_url, assignments_1.end_at AS assignments_1_end_at, assignments_1.course_id AS assignments_1_course_id, assignments_1.created_at AS assignments_1_created_at, assignments_1.updated_at AS assignments_1_updated_at

FROM submissions LEFT OUTER JOIN assignments AS assignments_1 ON assignments_1.id = submissions.assignment_id LEFT OUTER JOIN courses AS courses_1 ON courses_1.id = assignments_1.course_id ORDER BY submissions.updated_at
"""
    sessions = get_session()
    session = sessions.__next__()
    res = session.execute(q)
    for r in res:
        print(r)


if __name__ == "__main__":
    create_tables()
    make_superuser()
    # exec_pdo()

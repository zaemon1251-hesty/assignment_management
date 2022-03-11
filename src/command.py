from domain import AuthedUser
from infrastructure.cert import AuthDriverImpl
from infrastructure.postgresql.database import get_session, Base, engine
from infrastructure.postgresql.users import UserOrm
from sqlalchemy.orm.exc import NoResultFound
import os


async def make_superuser():
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


if __name__ == "__main__":
    create_tables()
    make_superuser()

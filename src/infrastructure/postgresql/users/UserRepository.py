import os
from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from src.domain.UserRepository import UserRepository
from src.domain.exception import TargetNotFoundException
from src.domain.user import User, AuthedUser
from src.infrastructure.postgresql.users.UserOrm import UserOrm
from src.usecase.users.UserUseCase import UserUseCaseUnitOfWork


class UserUseCaseUnitOfWorkImpl(UserUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
    ):
        self.session: Session = session
        self.user_repository: UserRepository = user_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class UserRepositoryImpl(UserRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch(self, id: int) -> Optional[User]:
        try:
            user_orm = self.session.query(UserOrm).filter_by(id=id).one()
            return user_orm.to_domain()
        except NoResultFound:
            return None
        except Exception as e:
            raise

    async def fetch_by_name(self, name: str) -> Optional[AuthedUser]:
        try:
            user_orm = self.session.query(UserOrm).filter_by(name=name).one()
            return user_orm.to__authed()
        except NoResultFound:
            return None
        except Exception:
            raise

    async def fetch_all(self, domain: Optional[User]) -> List[User]:
        targets = dict(domain) if domain is not None else {}
        try:
            q = self.session.query(UserOrm)
            for attr, value in targets.items():
                if attr == "id":
                    continue
                q = q.filter(getattr(UserOrm, attr) == value)
            q = q.order_by(UserOrm.updated_at)
            user_orms = q.all()
            return list(
                map(
                    lambda user_orm: user_orm.to_domain(),
                    user_orms
                )
            ) if len(user_orms) > 0 else []
        except Exception:
            raise

    async def create(self, domain: AuthedUser) -> User:
        try:
            user_orm = UserOrm.from_domain(domain)
            self.session.add(user_orm)
            return user_orm.to_domain()
        except Exception:
            raise

    async def update(self, domain: AuthedUser) -> User:
        try:
            user_orm = UserOrm.from_domain(domain)
            target = self.session.query(UserOrm).filter_by(id=domain.id).one()
            updatables = [
                "name",
                "email",
                "disabled",
                "hash_password",
                "update_at",
            ]
            for attr in updatables:
                value = getattr(user_orm, attr)
                if value is not None and value != "":
                    setattr(target, attr, value)
            return target.to_domain()
        except Exception:
            raise

    async def delete(self, id: int) -> bool:
        try:
            self.session.query(UserOrm).filter_by(id=id).delete()
            return True
        except Exception:
            raise

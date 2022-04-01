from typing import List
from src.infrastructure.postgresql.BaseService import make_conditions
from sqlalchemy.orm.session import Session
from sqlalchemy import or_, and_
from src.domain.user import User
from src.usecase.users import UserService, UserQueryModel
from src.infrastructure.postgresql.users import UserOrm


class UserServiceImpl(UserService):
    """User Service with postgreSQL

    Args:
        session (sqlalchemy.orm.Session): セッション
    """

    def __init__(self, session: Session):
        self.session: Session = session

    async def fetch_all(self, query: UserQueryModel) -> List[User]:
        targets = dict(query) if query is not None else {}
        try:
            and_filters = []
            q = self.session.query(UserOrm)
            for attr, value in targets.items():
                and_filters.append(make_conditions(UserOrm, attr, value))
            q = q.filter(and_(*and_filters))
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

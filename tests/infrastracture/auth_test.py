from typing import List, Optional
from domain.user import AuthedUser, User
from infrastructure.cert.auth import AuthDriverImpl
from domain.UserRepository import UserRepository
from usecase.token import Token, TokenData

user = User(
    id=1,
    name="test",
    email="test@example.com",
    disabled=False)

user2 = User(
    id=2,
    name="mori",
    email="awk@example.jp",
    disabled=False)


ad_user = AuthedUser(
    **user.dict(),
    hash_password=AuthDriverImpl.get_password_hash("password")
)


class UserRepositoryMock(UserRepository):

    async def fetch(id: int) -> Optional[User]:
        return user

    async def fetch_by_name(name: str = None) -> Optional[AuthedUser]:
        return ad_user

    async def fetch_all(domain: Optional[User]) -> List[User]:
        return [user, user2]

    async def create(domain: AuthedUser) -> User:
        return user

    async def update(domain: AuthedUser) -> User:
        return user

    async def delete(id: int) -> bool:
        return True


class AuthDriverImplTest:
    def __init__(self) -> None:
        self.driver = AuthDriverImpl(user_repository=UserRepositoryMock())

    def test_authenticate_password(self):
        assert self.driver.authenticate_password("password")

    async def test_create_access_token(self):
        token = await self.driver.create_access_token("test", "password")
        assert isinstance(token.access_token, str)

    async def test_authenticate_token(self):
        token: Token = await self.driver.create_access_token("test", "password")
        data: TokenData = await self.driver.authenticate_token(token)
        assert data.user_name == "test"

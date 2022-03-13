from datetime import datetime, timezone
import json
from passlib.context import CryptContext
import jwt
from pydantic import ValidationError
from src.domain.exception import CredentialsException, TargetNotFoundException, UnauthorizedException
from src.domain.user import AuthedUser, User
from src.usecase.driver.AuthDriver import AuthDriver, Token, TokenData
from src.domain.UserRepository import UserRepository
from src.settings import JWK, PRIVATE_PEM, TOKEN_EXPIRE
from src.settings import logger


class AuthDriverImpl(AuthDriver):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_access_token(self, name: str, password: str) -> Token:
        try:
            user: AuthedUser = await self.user_repository.fetch_by_name(name)
            if self.authenticate_password(password, user.hash_password):
                payload = TokenData(
                    user_name=user.name,
                    exp=TOKEN_EXPIRE.timestamp())
                token = jwt.encode(
                    dict(payload),
                    PRIVATE_PEM,
                    algorithm=JWK["keys"][0]["alg"],
                    headers={"kid": JWK["keys"][0]["kid"]}
                )
                return Token(access_token=token, token_type="Bearer")
            else:
                raise UnauthorizedException(
                    "Not the correct password: user-name '%s'" % name)
        except TargetNotFoundException:
            raise UnauthorizedException(
                "User Not Found. please confirm this user-name is right: '%s'" %
                name)

    async def get_user_by_token(self, token: str) -> User:
        try:
            payload = self.authenticate_token(token)
            user = self.user_repository.fetch_by_name(payload.user_name)
        except ValidationError or ValueError:
            raise CredentialsException("token has wrong payload.")
        return user

    @classmethod
    def authenticate_password(
            cls,
            password: str,
            hashed_password: str) -> bool:
        if not cls.verify_password(password, hashed_password):
            return False
        return True

    @classmethod
    def authenticate_token(
            cls,
            token: str) -> TokenData:
        if token:
            auth = token.split(" ")
        if len(auth) != 2:
            raise CredentialsException("token format something wrong.")
        if auth[0] != "Bearer":
            raise CredentialsException(
                "token-type not acceptable. please use Bearer")
        id_token = auth[1]
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(
            json.dumps(JWK["keys"][0]))

        try:
            payload = jwt.decode(
                id_token,
                public_key,
                algorituhms=JWK["keys"][0]["alg"])
            payload = TokenData(**payload)
            if payload.exp <= datetime.utcnow().timestamp():
                raise CredentialsException("this token has expired.")
        except Exception:
            CredentialsException("something went wrong.")
        return payload

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        return cls.pwd_context.verify(plain_password, hashed_password)

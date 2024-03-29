from datetime import datetime
import json
import re
import traceback
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm.session import Session

from src.domain import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException, UnauthorizedException
from src.settings import logger
from src.usecase.token import Token
from src.usecase.users import UserUseCase, UserUseCaseImpl, UserUseCaseUnitOfWork
from src.domain import AuthedUser, User
from src.infrastructure.cert.auth import AuthDriverImpl
from src.infrastructure.postgresql.database import get_session
from src.infrastructure.postgresql.users import UserRepositoryImpl, UserUseCaseUnitOfWorkImpl, UserServiceImpl
from src.usecase.users import UserUseCase, UserUseCaseImpl, UserUseCaseUnitOfWork, UserCommandModel, UserQueryModel
from src.interface.presenter.ProcessRequest import process_users_query
from src.domain import UserRepository

from fastapi.security import APIKeyHeader
api_key = APIKeyHeader(name="Authorization", auto_error=False)


user_api_router = APIRouter(prefix="/users")


def _user_usecase(session: Session = Depends(get_session)) -> UserUseCase:
    user_repository: UserRepository = UserRepositoryImpl(session)
    uow: UserUseCaseUnitOfWork = UserUseCaseUnitOfWorkImpl(
        session, user_repository=user_repository
    )
    return UserUseCaseImpl(
        UserServiceImpl(session),
        uow,
        AuthDriverImpl(user_repository)
    )


@user_api_router.get(
    "/{user_id}",
    response_model=Optional[User],
    status_code=status.HTTP_200_OK,
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def get(user_id: int, user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user = await user_usecase.fetch(user_id)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return user


@user_api_router.get(
    "/_authenticate",
    response_model=Optional[AuthedUser],
    status_code=status.HTTP_200_OK,
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def authorize_user(token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user = user_usecase.fetch_by_token(token)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return user


@user_api_router.get(
    "/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        name: Optional[str] = None,
        disabled: Optional[bool] = None,
        user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        query = UserQueryModel(
            name=name,
            disabled=disabled
        )
        users = await user_usecase.fetch_all(query)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return users


@user_api_router.post(
    "/add",
    response_model=UserCommandModel,
    status_code=status.HTTP_200_OK,
    # responses={
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "already exists",
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorized this manipulate"
    #     }
    # }
)
async def create(user_data: UserCommandModel, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        user = await user_usecase.create(user_data)
    except TargetAlreadyExsitException as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    except CredentialsException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return user


@user_api_router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_202_ACCEPTED,
    # responses={
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "id contradicts with this data",
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorize this manipulate"
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def update(user_id: int, user_data: UserCommandModel, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        user = await user_usecase.update(user_id, user_data)
    except CredentialsException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return user


@user_api_router.patch(
    "/change_password/{user_id}",
    response_model=User,
    status_code=status.HTTP_202_ACCEPTED,
    # responses={
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "id contradicts with this data",
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorize this manipulate"
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def change_password(user_id: int, password: str, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        mdl = UserCommandModel(
            password=password
        )
        user = await user_usecase.update(user_id, mdl)
    except CredentialsException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return user


@user_api_router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    # response={
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorized this manipulate"
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def delete(user_id: int, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        await user_usecase.delete(user_id)
    except CredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_api_router.post(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Token,
    # response={
    #     status.HTTP_401_UNAUTHORIZED: {
    #         "model": "failed to create token for some reasons."
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def create_token(name: str = Form(""), password: str = Form(""), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        token: Token = await user_usecase.create_token(name, password)
        return token
    except UnauthorizedException as e:
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

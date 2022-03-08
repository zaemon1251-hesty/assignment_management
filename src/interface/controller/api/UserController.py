from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from logging import config

from src.usecase.users.UserUseCase import UserUseCase
from src.domain.user import User

user_api_router = APIRouter()


config.fileConfig("error.log", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_user_usecase: UserUseCase


@user_api_router.get(
    "/{user_id}",
    response_model=Optional[User],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def get(user_id: int, user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user = user_usecase.fetch(user_id)
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
async def get_all(user_data: Optional[User], user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        users = user_usecase.fetch_all(user_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return users


@user_api_router.post(
    "/add",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def create(user_data: User, auth_data: Dict, user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user = user_usecase.create(user_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return user


@user_api_router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "id contradicts with data",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def update(user_id: int, user_data: User, auth_data: Dict, user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user = user_usecase.update(user_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return user


@user_api_router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response={
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorized this manipulate"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def delete(user_id: int, auth_data: Dict, user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.delete(user_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_api_router.post(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
    response={
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorized this manipulate"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def login(user_id: int, auth_data: Dict, user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_id = auth_data.get('id')
        user_password = auth_data.get('password')
        user_usecase.login(user_id, user_password)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

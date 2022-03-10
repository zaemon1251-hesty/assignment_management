from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import APIKeyHeader
from src.domain.exception import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException, UnauthorizedException
from src.settings import logger
from src.usecase.token import Token
from src.usecase.users.UserUseCase import UserUseCase
from src.domain.user import AuthedUser, User
from src.interface.controller.ApiController import api_key


user_api_router = APIRouter()

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
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
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
    responses={
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "already exists",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorized this manipulate"
        }
    }
)
async def create(user_data: User, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        user = user_usecase.create(user_data)
    except TargetAlreadyExsitException as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    except CredentialsException as e:
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
    responses={
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "id contradicts with this data",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorize this manipulate"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def update(user_id: int, user_data: User, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        if user_id != user_data.id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        user = user_usecase.update(user_id, user_data)
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
async def delete(user_id: int, token: str = Depends(api_key), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        user_usecase.delete(user_id)
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
    response={
        status.HTTP_401_UNAUTHORIZED: {
            "model": "failed to create token for some reasons."
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def create_token(name: Form(""), password: Form(""), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        token: Token = await user_usecase.create_token(name, password)
        return token
    except UnauthorizedException as e:
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

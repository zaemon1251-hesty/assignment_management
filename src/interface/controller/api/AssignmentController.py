from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional
from src.domain.exception import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException

from src.settings import logger
from src.domain.assignment import ASSIGNMENT_STATE, Assignment
from src.interface.controller.ApiController import api_key
from src.usecase.users.UserUseCase import UserUseCase
from src.usecase.assignments.AssignmentUseCase import AssignmentUseCase

assignment_api_router = APIRouter()

_assignment_usecase: AssignmentUseCase

_user_usecase: UserUseCase


@assignment_api_router.get(
    "/{assignment_id}",
    response_model=Optional[Assignment],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def get(assignment_id: Optional[int], assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = assignment_usecase.fetch(assignment_id)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return assignment


@assignment_api_router.get(
    "/",
    response_model=List[Assignment],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def get_all(assignment_data: Optional[Assignment], assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = assignment_usecase.fetch_all(assignment_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return assignment


@assignment_api_router.post(
    "/add",
    response_model=Assignment,
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
async def add(assignment_data: Assignment, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        assignment = assignment_usecase.add(assignment_data)
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return assignment


@assignment_api_router.put(
    "/{assingnment_id}",
    response_model=Assignment,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "id contradicts with data",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorized this manipulate"
        }
    }
)
async def update(assingnment_id: int, assignment_data: Assignment, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        if assingnment_id != assignment_data.id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        assignment = assignment_usecase.update(assignment_data)
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
    return assignment


@assignment_api_router.patch(
    "/change/{assignment_id}/{state}",
    response_model=Assignment,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorized this manipulate"
        }
    }
)
async def change_state(assignment_id: int, state: int, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        _assignment_target: Assignment = assignment_usecase.fetch(
            assignment_id)
        _assignment_target.state = ASSIGNMENT_STATE(state)
        assignment = assignment_usecase.update(_assignment_target)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except CredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return assignment


@assignment_api_router.delete(
    "/{assignment_id}",
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
async def delete(assignment_id: int, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        assignment_usecase.delete(assignment_id)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except CredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

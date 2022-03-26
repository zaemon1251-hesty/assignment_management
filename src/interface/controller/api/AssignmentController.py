from datetime import datetime
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional

from src.domain import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException
from src.settings import logger
from src.domain import ASSIGNMENT_STATE, Assignment
from .UserController import api_key, _user_usecase
from src.usecase.users.UserUseCase import UserUseCase
from src.usecase.assignments.AssignmentUseCase import AssignmentCommandModel, AssignmentUseCase

from src.infrastructure.postgresql.database import get_session
from src.infrastructure.postgresql.assignments import AssignmentRepositoryImpl, AssignmentUseCaseUnitOfWorkImpl
from src.usecase.assignments import AssignmentUseCase, AssignmentUseCaseImpl, AssignmentUseCaseUnitOfWork
from src.domain import AssignmentRepository
from sqlalchemy.orm.session import Session

assignment_api_router = APIRouter(prefix="/assignments")


def _assignment_usecase(session: Session = Depends(
        get_session)) -> AssignmentUseCase:
    assignment_repository: AssignmentRepository = AssignmentRepositoryImpl(
        session)
    uow: AssignmentUseCaseUnitOfWork = AssignmentUseCaseUnitOfWorkImpl(
        session, assignment_repository=assignment_repository
    )
    return AssignmentUseCaseImpl(uow)


@assignment_api_router.get(
    "/{assignment_id}",
    response_model=Optional[Assignment],
    status_code=status.HTTP_200_OK,
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def get(assignment_id: Optional[int], assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = await assignment_usecase.fetch(assignment_id)
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
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def get_all(assignment_data: Optional[Assignment] = None, assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = await assignment_usecase.fetch_all(assignment_data)
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return assignment


@assignment_api_router.post(
    "/add",
    response_model=Assignment,
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
async def add(assignment_data: Assignment, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        assignment = await assignment_usecase.add(assignment_data)
    except TargetAlreadyExsitException as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    except CredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return assignment


@assignment_api_router.put(
    "/{assingnment_id}",
    response_model=Assignment,
    status_code=status.HTTP_202_ACCEPTED,
    # responses={
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "id contradicts with data",
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorized this manipulate"
    #     }
    # }
)
async def update(assingnment_id: int, assignment_data: AssignmentCommandModel, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        assignment = await assignment_usecase.update(assingnment_id, assignment_data)
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
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorized this manipulate"
    #     }
    # }
)
async def change_state(assignment_id: int, state: int, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        _assignment_target: Assignment = AssignmentCommandModel(
            state=ASSIGNMENT_STATE(state))
        assignment = await assignment_usecase.update(assignment_id, _assignment_target)
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
    # response={
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorized this manipulate"
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def delete(assignment_id: int, token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        await assignment_usecase.delete(assignment_id)
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


@assignment_api_router.get(
    "/check_expire",
    status_code=status.HTTP_202_ACCEPTED,
    # responses={
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "id contradicts with data",
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": "unauthorized this manipulate"
    #     }
    # }
)
async def check_expire(token: str = Depends(api_key), assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        today = datetime.utcnow()
        assignment_cond = Assignment(
            state=ASSIGNMENT_STATE.ALIVE, end_at=today)
        assignments: List[Assignment] = await assignment_usecase.fetch_all(assignment_cond)
        for assignment in assignments:
            assignment.state = ASSIGNMENT_STATE.DEAD
            await assignment_usecase.update(assignment)
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

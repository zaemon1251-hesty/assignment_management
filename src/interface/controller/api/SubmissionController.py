from fastapi import APIRouter
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from domain.exception import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException
from settings import logger
from domain.submission import SUBMISSION_STATE, Submission
from domain.user import User
from usecase.submissions.SubmissionUseCase import SubmissionUseCase
from .UserController import api_key
from usecase.users.UserUseCase import UserUseCase

from infrastructure.postgresql.database import get_session
from infrastructure.postgresql.submissions.SubmissionRepository import SubmissionRepositoryImpl, SubmissionUseCaseUnitOfWorkImpl
from usecase.submissions.SubmissionUseCase import SubmissionUseCase, SubmissionUseCaseImpl, SubmissionUseCaseUnitOfWork
from domain.SubmissionRepository import SubmissionRepository
from sqlalchemy.orm.session import Session
from interface.controller.api.UserController import _user_usecase


submission_api_router = APIRouter(prefix="/submissions")


def _submission_usecase(session: Session = Depends(
        get_session)) -> SubmissionUseCase:
    submission_repository: SubmissionRepository = SubmissionRepositoryImpl(
        session)
    uow: SubmissionUseCaseUnitOfWork = SubmissionUseCaseUnitOfWorkImpl(
        session, submission_repository=submission_repository
    )
    return SubmissionUseCaseImpl(uow)


@submission_api_router.get(
    "/{submission_id}",
    response_model=Optional[Submission],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def get(submission_id: int, submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        submission = await submission_usecase.fetch(submission_id)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return submission


@submission_api_router.get(
    "/",
    response_model=List[Submission],
    status_code=status.HTTP_200_OK,
)
async def get_all(submission_data: Optional[Submission], submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        submissions = await submission_usecase.fetch_all(submission_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return submissions


@submission_api_router.post(
    "/add",
    response_model=Submission,
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
async def add(submission_data: Submission, token: str = Depends(api_key), submission_usecase: SubmissionUseCase = Depends(_submission_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        submission = await submission_usecase.add(submission_data)
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
    return submission


@submission_api_router.put(
    "/{submission_id}",
    response_model=Submission,
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
async def update(submission_id: int, submission_data: Submission, token: str = Depends(api_key), submission_usecase: SubmissionUseCase = Depends(_submission_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        if submission_id != submission_data.id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        submission = await submission_usecase.update(submission_data)
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
    return submission


@submission_api_router.patch(
    "/change/{submission_id}/{state}",
    response_model=Submission,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": "unauthorized this manipulate"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def change_state(submission_id: int, state: int, token: str = Depends(api_key), submission_usecase: SubmissionUseCase = Depends(_submission_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        _submission_target: Submission = submission_usecase.fetch(
            submission_id)
        _submission_target.state = SUBMISSION_STATE(state)
        submission = await submission_usecase.update(_submission_target)
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
    return submission


@submission_api_router.delete(
    "/{submission_id}",
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
async def delete(submission_id: int, token: str = Depends(api_key), submission_usecase: SubmissionUseCase = Depends(_submission_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        await submission_usecase.delete(submission_id)
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

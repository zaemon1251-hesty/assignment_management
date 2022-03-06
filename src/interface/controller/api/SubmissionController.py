from fastapi import APIRouter
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from logging import config

from src.domain.submission import Submission
from src.domain.user import User
from src.usecase.submissions.SubmissionUseCase import SubmissionUseCase

submission_api_router = APIRouter()

config.fileConfig("error.log", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_submission_usecase: SubmissionUseCase


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
        submission = submission_usecase.fetch(submission_id)
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
        submissions = submission_usecase.fetch_all(submission_data)
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
)
async def add(submission_data: Submission, auth_data: Dict, submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        submission = submission_usecase.add(submission_data)
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
        }
    }
)
async def update(submission_id: int, submission_data: Submission, auth_data: Dict, submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        submission = submission_usecase.update(submission_data)
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
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "id contradicts with data",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def change_state(submission_id: int, state: int, auth_data: Dict, submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        _submission_target: Submission
        submission = submission_usecase.update(_submission_target)
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
async def delete(submission_id: int, auth_data: Dict, submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        submission_usecase.delete(submission_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@submission_api_router.post(
    "/scraping",
    status_code=status.HTTP_200_OK,
)
async def scraping(auth_data: Dict, submission_usecase: SubmissionUseCase = Depends(_submission_usecase)):
    try:
        login_user: User
        submission_usecase.scraping_add(login_user)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

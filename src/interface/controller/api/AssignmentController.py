from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional

import logging
from logging import config
from src.domain.assignment import Assignment

from src.usecase.assignments.AssignmentUseCase import AssignmentUseCase

assignment_api_router = APIRouter()

config.fileConfig("error.log", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_assignment_usecase: AssignmentUseCase


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
async def get(assignment_id: Optional[int], assignment_data: Assignment, assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = assignment_usecase.fetch(assignment_id)
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
)
async def add(assignment_data: Assignment, auth_data: Dict, assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = assignment_usecase.add(assignment_data)
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
        }
    }
)
async def update(assingnment_id: int, assignment_data: Assignment, auth_data: Dict, assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment = assignment_usecase.update(assignment_data)
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
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "id contradicts with data",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def change_state(assignment_id: int, state: int, auth_data: Dict, assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        _assignment_target: Assignment
        assignment = assignment_usecase.update(_assignment_target)
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
async def delete(assignment_id: int, auth_data: Dict, assignment_usecase: AssignmentUseCase = Depends(_assignment_usecase)):
    try:
        assignment_usecase.delete(assignment_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

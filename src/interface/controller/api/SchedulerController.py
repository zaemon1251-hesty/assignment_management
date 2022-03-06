from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional

import logging
from logging import config
from src.domain.scheduler import Scheduler

from src.usecase.schedulers.SchedulerUseCase import SchedulerUseCase

scheduler_api_router = APIRouter()

config.fileConfig("error.log", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_scheduler_usecase: SchedulerUseCase


@scheduler_api_router.get(
    "/{scheduler_id}",
    response_model=Optional[Scheduler],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def get(scheduler_id: int, scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        scheduler = scheduler_usecase.fetch(scheduler_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return scheduler


@scheduler_api_router.get(
    "/",
    response_model=List[Scheduler],
    status_code=status.HTTP_200_OK,
)
async def get_all(scheduler_data: Optional[Scheduler], scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        schedulers = scheduler_usecase.fetch_all(scheduler_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return schedulers


@scheduler_api_router.post(
    "/add",
    response_model=Scheduler,
    status_code=status.HTTP_200_OK,
)
async def create(scheduler_data: Scheduler, auth_data: Dict, scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        scheduler = scheduler_usecase.create(scheduler_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return scheduler


@scheduler_api_router.put(
    "/{scheduler_id}",
    response_model=Scheduler,
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
async def update(scheduler_id: int, scheduler_data: Scheduler, auth_data: Dict, scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        scheduler = scheduler_usecase.update(scheduler_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return scheduler


@scheduler_api_router.post(
    "/change/{scheduler_id}/{state}",
    response_model=Scheduler,
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
async def change_state(scheduler_id: int, state: int, auth_data: Dict, scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        _scheduler_target: Scheduler
        scheduler = scheduler_usecase.update(_scheduler_target)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return scheduler


@scheduler_api_router.delete(
    "/{scheduler_id}",
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
async def delete(scheduler_id: int, auth_data: Dict, scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        scheduler_usecase.delete(scheduler_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@scheduler_api_router.get(
    "/deadline_reminder",
    status_code=status.HTTP_200_OK
)
async def deadline_reminder(scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        scheduler_usecase.deadline_reminder()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

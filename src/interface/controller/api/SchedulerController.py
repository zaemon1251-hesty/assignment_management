from datetime import datetime, timedelta
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional

from src.infrastructure.postgresql.submissions import SubmissionServiceImpl, SubmissionRepositoryImpl
from src.infrastructure.postgresql.users.UserRepository import UserRepositoryImpl
from src.domain import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException
from src.settings import logger
from src.domain import Scheduler, SchedulerRepository, SubmissionRepository, UserRepository
from src.usecase.schedulers import SchedulerUseCase
from .UserController import api_key, _user_usecase
from src.usecase.users import UserUseCase
from src.infrastructure.mail import NotifyDriverImpl
from src.infrastructure.postgresql.database import get_session
from src.infrastructure.postgresql.schedulers import SchedulerRepositoryImpl, SchedulerUseCaseUnitOfWorkImpl, SchedulerServiceImpl
from src.usecase.schedulers import SchedulerUseCase, SchedulerUseCaseImpl, SchedulerUseCaseUnitOfWork, SchedulerCommandModel, SchedulerQueryModel, SchedulerService
from sqlalchemy.orm.session import Session


scheduler_api_router = APIRouter(prefix="/schedulers")


def _scheduler_usecase(session: Session = Depends(
        get_session)) -> SchedulerUseCase:
    scheduler_repository: SchedulerRepository = SchedulerRepositoryImpl(
        session)
    submission_repository: SubmissionRepository = SubmissionRepositoryImpl(
        session)
    user_repository: UserRepository = UserRepositoryImpl(
        session)
    uow: SchedulerUseCaseUnitOfWork = SchedulerUseCaseUnitOfWorkImpl(
        session,
        scheduler_repository=scheduler_repository,
        submission_repository=submission_repository,
        user_repository=user_repository,
    )
    return SchedulerUseCaseImpl(
        uow,
        SchedulerServiceImpl(session),
        SubmissionServiceImpl(session),
        NotifyDriverImpl()
    )


@scheduler_api_router.get(
    "/{scheduler_id}",
    response_model=Optional[Scheduler],
    status_code=status.HTTP_200_OK,
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def get(scheduler_id: int, scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        scheduler = await scheduler_usecase.fetch(scheduler_id)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
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
async def get_all(
        submission_id: Optional[int] = None,
        reminded: Optional[bool] = None,
        remind_at: Optional[datetime] = None,
        remind_af: Optional[datetime] = None,
        remind_be: Optional[datetime] = None,
        scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        query = SchedulerQueryModel(
            submission_id=submission_id,
            reminded=reminded,
            remind_at=[remind_at] if remind_at is not None else None,
            remind_af=remind_af,
            remind_be=remind_be
        )
        schedulers = await scheduler_usecase.fetch_all(query)
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return schedulers


@scheduler_api_router.post(
    "/add",
    response_model=Scheduler,
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
async def add(scheduler_data: Scheduler, token: str = Depends(api_key), scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        scheduler = await scheduler_usecase.add(scheduler_data)
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
    return scheduler


@scheduler_api_router.put(
    "/{scheduler_id}",
    response_model=Scheduler,
    status_code=status.HTTP_202_ACCEPTED,
    # responses={
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "id contradicts with data",
    #     },
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     },
    #     status.HTTP_406_NOT_ACCEPTABLE: {
    #         "model": "id contradicts with data",
    #     }
    # }
)
async def update(scheduler_id: int, scheduler_data: SchedulerCommandModel, token: str = Depends(api_key), scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        scheduler = await scheduler_usecase.update(scheduler_id, scheduler_data)
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
    return scheduler


@scheduler_api_router.delete(
    "/{scheduler_id}",
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
async def delete(scheduler_id: int, token: str = Depends(api_key), scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        scheduler_usecase.delete(scheduler_id)
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


@scheduler_api_router.post(
    "/deadline_reminder",
    status_code=status.HTTP_200_OK
)
async def deadline_reminder(scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase)):
    try:
        flg = await scheduler_usecase.deadline_reminder()
        return flg
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


@scheduler_api_router.post(
    "/add_remind_schdule",
    status_code=status.HTTP_200_OK
)
async def add_remind_schedule(by: Optional[timedelta] = None, token: str = Depends(api_key), scheduler_usecase: SchedulerUseCase = Depends(_scheduler_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        schdulers = await scheduler_usecase.add_remind_schedule(by=by)
        return {"added_schedules": len(schdulers)}
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

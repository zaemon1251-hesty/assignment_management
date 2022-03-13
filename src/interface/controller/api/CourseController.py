from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional
from src.domain import Course
from src.domain import CredentialsException, TargetAlreadyExsitException, TargetNotFoundException
from src.settings import logger
from src.usecase.courses import CourseUseCase
from .UserController import api_key, _user_usecase
from src.usecase.users import UserUseCase
from src.infrastructure.crawl import ScrapeDriverImpl
from src.infrastructure.postgresql.database import get_session
from src.infrastructure.postgresql.courses.CourseRepository import CourseRepositoryImpl, CourseUseCaseUnitOfWorkImpl
from src.usecase.courses.CourseUseCase import CourseUseCase, CourseUseCaseImpl, CourseUseCaseUnitOfWork
from src.domain.CourseRepository import CourseRepository
from sqlalchemy.orm.session import Session


course_api_router = APIRouter(prefix="/courses")


def _course_usecase(session: Session = Depends(get_session)) -> CourseUseCase:
    course_repository: CourseRepository = CourseRepositoryImpl(session)
    uow: CourseUseCaseUnitOfWork = CourseUseCaseUnitOfWorkImpl(
        session, course_repository=course_repository
    )
    return CourseUseCaseImpl(uow, ScrapeDriverImpl())


@course_api_router.get(
    "/{course_id}",
    response_model=Optional[Course],
    status_code=status.HTTP_200_OK,
    # responses={
    #     status.HTTP_404_NOT_FOUND: {
    #         "model": "not found"
    #     }
    # }
)
async def get(course_id: int, course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        course = await course_usecase.fetch(course_id)
    except TargetNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return course


@course_api_router.get(
    "/",
    response_model=List[Course],
    status_code=status.HTTP_200_OK,
)
async def get_all(course_data: Optional[Course], course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        courses = await course_usecase.fetch_all(course_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return courses


@course_api_router.post(
    "/add",
    response_model=Course,
    status_code=status.HTTP_200_OK,
)
async def add(course_data: Course, token: str = Depends(api_key), course_usecase: CourseUseCase = Depends(_course_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        course = await course_usecase.add(course_data)
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
    return course


@course_api_router.put(
    "/{course_id}",
    response_model=Course,
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
async def update(course_id: int, course_data: Course, token: str = Depends(api_key), course_usecase: CourseUseCase = Depends(_course_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        if course_id != course_data.id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        course = await course_usecase.update(course_data)
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
    return course


@course_api_router.delete(
    "/{course_id}",
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
async def delete(course_id: int, token: str = Depends(api_key), course_usecase: CourseUseCase = Depends(_course_usecase), user_usecase: UserUseCase = Depends(_user_usecase)):
    try:
        user_usecase.auth_verify(token)
        await course_usecase.delete(course_id)
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


@course_api_router.get(
    "/auto_scraping",
    status_code=status.HTTP_200_OK
)
async def scraping(course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        flg = await course_usecase.periodically_scraper()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

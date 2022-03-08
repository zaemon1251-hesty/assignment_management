from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional

import logging
from logging import config
from src.domain.course import Course

from src.usecase.courses.CourseUseCase import CourseUseCase

course_api_router = APIRouter()

config.fileConfig("error.log", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_course_usecase: CourseUseCase


@course_api_router.get(
    "/{course_id}",
    response_model=Optional[Course],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def get(course_id: int, course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        course = course_usecase.fetch(course_id)
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
        courses = course_usecase.fetch_all(course_data)
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
async def create(course_data: Course, auth_data: Dict, course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        course = course_usecase.create(course_data)
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
    responses={
        status.HTTP_406_NOT_ACCEPTABLE: {
            "model": "id contradicts with data",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": "not found"
        }
    }
)
async def update(course_id: int, course_data: Course, auth_data: Dict, course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        course = course_usecase.update(course_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return course


@course_api_router.post(
    "/change/{course_id}/{state}",
    response_model=Course,
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
async def change_state(course_id: int, state: int, auth_data: Dict, course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        _course_target: Course
        course = course_usecase.update(_course_target)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return course


@course_api_router.delete(
    "/{course_id}",
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
async def delete(course_id: int, auth_data: Dict, course_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        course_usecase.delete(course_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@course_api_router.get(
    "/auto_scraping",
    status_code=status.HTTP_200_OK
)
async def scraping(user_usecase: CourseUseCase = Depends(_course_usecase)):
    try:
        user_usecase.periodically_scraper()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

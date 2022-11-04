from src.interface.controller.api import assignment_api_router, user_api_router, course_api_router, submission_api_router, scheduler_api_router
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse


api_router = APIRouter(prefix="/api")

routers = {}

routers["assignments"] = assignment_api_router
routers["users"] = user_api_router
routers["courses"] = course_api_router
routers["submissions"] = submission_api_router
routers["schedulers"] = scheduler_api_router

for router_name, router in routers.items():
    api_router.include_router(router)


@api_router.get(
    "/",
    status_code=status.HTTP_302_FOUND
)
async def redirects():
    return {"api": "root"}


@api_router.post(
    "/judge_graduate",
    status_code=status.HTTP_200_OK
)
async def judge_graduate():
    
    return

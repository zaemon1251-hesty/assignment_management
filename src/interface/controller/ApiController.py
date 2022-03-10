from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader


from src.interface.controller.api import (
    assignment_api_router,
    user_api_router,
    course_api_router,
    submission_api_router,
    scheduler_api_router
)

api_router = APIRouter()

routers = {}

routers["/assignmets"] = assignment_api_router
routers["/users"] = user_api_router
routers["/courses"] = course_api_router
routers["/submissions"] = submission_api_router
routers["/schedulers"] = scheduler_api_router

api_key = APIKeyHeader(name="Authorization", auto_error=False)

for router_name, router in routers.items():
    api_router.include_router(router, prefix=router_name)


@api_router.get(
    "/",
    status_code=status.HTTP_302_FOUND
)
async def redirects():
    return RedirectResponse(api_router.url_path_for("/"), status_code=302)

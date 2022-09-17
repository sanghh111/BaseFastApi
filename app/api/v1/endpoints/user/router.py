from fastapi import APIRouter
from app.api.v1.endpoints.user import view as views_user

router_module = APIRouter()

router_module.include_router(router=views_user.router, tags=["User"])

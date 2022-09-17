from fastapi import APIRouter
from app.api.v1.endpoints.user import router as routers_user

router = APIRouter()
# Example
router.include_router(router=routers_user.router_module, prefix="/users")

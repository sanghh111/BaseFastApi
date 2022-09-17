from fastapi import APIRouter
from app.api.base.openapi import openapi_response
from app.api.base.schema import ResponseData
from app.api.v1.endpoints.user.controller import CtrUser
from app.api.v1.endpoints.user.schema.user import UserInfoResponse

router = APIRouter()


@router.post(
    path="/",
    name="Profile",
    description="Xem hồ sơ nhân viên",
    responses=openapi_response(UserInfoResponse)
)
async def view_profile(user_id: str) -> ResponseData[UserInfoResponse]:

    data = await CtrUser(is_init_postgres_session=False).ctr_profile(user_id=user_id)
    return ResponseData[UserInfoResponse](**data)

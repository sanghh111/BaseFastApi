from typing import Optional
from pydantic import Field
from app.api.base.schema import BaseSchema


# Request
# request model -->

########################################################################################################################
# Response
########################################################################################################################
# Response model -->
class UserInfoResponse(BaseSchema):
    username: str = Field(None, description='Username người dùng')
    name: str = Field(None, description='Họ và tên người dùng')
    code: str = Field(None, description='Mã nhân viên')
    avatar_url: str = Field(None, description='Avatar url')
    token: str = Field(..., description='Token')
    email: Optional[str] = Field(None, description='Email')


from typing import Optional

from pydantic import Field, validator
from pydantic.schema import datetime

from app.api.base.schema import BaseSchema


# Request
class DropdownRequest(BaseSchema):
    id: str = Field(..., min_length=1, description='`Chuỗi định danh`')


class OptionalDropdownRequest(BaseSchema):
    id: Optional[str] = Field(None, min_length=1, description='`Chuỗi định danh`', nullable=True)


########################################################################################################################
# Response
########################################################################################################################
class DropdownResponse(BaseSchema):
    id: str = Field(..., min_length=1, description='`Chuỗi định danh`')
    code: str = Field(..., min_length=1, description='`Mã`')
    name: str = Field(..., min_length=1, description='`Tên`')


class OptionalDropdownResponse(BaseSchema):
    id: Optional[str] = Field(None, description='`Chuỗi định danh`', nullable=True)
    code: Optional[str] = Field(None, description='`Mã`', nullable=True)
    name: Optional[str] = Field(None, description='`Tên`', nullable=True)

    @validator('*')
    def check_blank_str(string):
        if string == '':
            return None
        return string


class HistoryData(BaseSchema):
    description: str = Field(..., description="Mô tả")
    created_at: datetime = Field(..., description="Bắt đầu lúc")
    completed_at: datetime = Field(..., description="Kết thúc lúc")
    status: int = Field(..., description="Trạng thái")
    # todo
    # thong tin ghi log kafka

from typing import List, Optional

import inflection as inflection
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn

from app.utils.error_messages import ERROR_ID_NOT_EXIST, ERROR_INVALID_NUMBER
from app.utils.functions import (is_valid_number)


async def repos_get_model_object_by_id_or_code(model_id: Optional[str], model_code: Optional[str],
                                        
                                               model,
                                               
                                               loc: str, session: Session, active_flag_actived=None) -> ReposReturn:
    statement = None

    if model_id:
        statement = select(model).filter(model.id == model_id)

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == active_flag_actived)

    obj = session.execute(statement).scalar()
    if not obj:
        if not loc:
            loc = f'{str(model.tablename)}_{"id" if model_id else "code"}'

        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=loc
        )

    return ReposReturn(data=obj)


async def repos_get_model_objects_by_ids(model_ids: List[str],
                                         
                                               model,
                                               
                                        session: Session,
                                         loc: Optional[str] = None) -> ReposReturn:
    """
    Get model objects by ids
    Chỉ cần truyền vào list id -> hàm sẽ tự chuyển về set(model_ids)
    :param model_ids: danh sách các id cần lấy ra model object
    :param model: model trong DB
    :param loc: vị trí lỗi
    :param session: phiên làm việc với DB bên controller
    :return:
    """
    model_ids = set(model_ids)

    statement = select(model).filter(model.id.in_(model_ids))

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    objs = session.execute(statement).scalars().all()
    if len(objs) != len(model_ids):
        obj_ids = [obj.id for obj in objs]
        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=f'{inflection.tableize(str(model.id))}, {model_ids - model_ids.intersection(set(obj_ids))}' if not
            loc else loc
        )

    return ReposReturn(data=objs)


async def get_optional_model_object_by_code_or_name(
        
        model,
        
        session: Session, model_id: Optional[str] = None,
        model_code: Optional[str] = None, model_name: Optional[str] = None
) -> Optional[object]:
    statement = None

    if model_id:
        statement = select(model).filter(model.id == model_id)

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if model_name:
        statement = select(model).filter(func.lower(model.name) == func.lower(model_name))  # TODO: check it

    if statement is None:
        return None

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    return session.execute(statement).scalar()


async def repos_is_valid_number(string: str, loc: str):
    if is_valid_number(string):
        return ReposReturn(data=None)

    return ReposReturn(is_error=True, msg=ERROR_INVALID_NUMBER, loc=loc)



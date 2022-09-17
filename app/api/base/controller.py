from datetime import date
from typing import List, Optional, Union
# logger
from loguru import logger
from starlette import status
from app.api.base.except_custom import ExceptionHandle
from app.api.base.repository import ReposReturn
from app.api.base.schema import Error
from app.api.base.validator import ValidatorReturn
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name,
    repos_get_model_object_by_id_or_code, repos_get_model_objects_by_ids
)
from app.utils.error_messages import (
    ERROR_ISSUED_DATE,
)
from app.utils.functions import (
    datetime_to_string, dropdown, dropdown_name, now, today
)

# example response model
from app.api.v1.endpoints.user.schema.user import UserInfoResponse




class BaseController(

):
    """
    BaseController use business
    """

    def __init__(self, current_user=None,
                 pagination_params=None,
                 is_init_postgres_session=True):
    
        self.current_user = current_user
        self.pagination_params = pagination_params
        self.errors = []


    def _close_postgres_session(self):

        pass


    def call_validator(self, result_call_validator: ValidatorReturn):
        if result_call_validator.is_error:
            self.response_exception(
                msg=result_call_validator.msg,
                loc=result_call_validator.loc,
                detail=result_call_validator.detail
            )

        return result_call_validator.data

    def call_repos(self, result_call_repos: ReposReturn):
        if result_call_repos.is_error:
            self.response_exception(
                msg=result_call_repos.msg,
                loc=result_call_repos.loc,
                detail=result_call_repos.detail,
                error_status_code=result_call_repos.error_status_code
            )

        return result_call_repos.data

    def append_error(self, msg: str, loc: str = "", detail: str = ""):
        """
        Hàm add exception để trả về
        :param msg: code exception
        :param loc: fields cần thông báo
        :param detail: Thông tin thông báo
        :return:
        """
        self.errors.append(Error(msg=msg, detail=detail, loc=loc))

    def _raise_exception(self, error_status_code=status.HTTP_400_BAD_REQUEST, data=None):
        errors = []
        for temp in self.errors:
            errors.append(temp.dict())
        raise ExceptionHandle(errors=errors, status_code=error_status_code, data=data)

    def response_exception(self, msg, loc="", detail="", error_status_code=status.HTTP_400_BAD_REQUEST, data=None):
        self._close_postgres_session()

        self.append_error(msg=msg, loc=loc, detail=detail)
        self._raise_exception(error_status_code=error_status_code, data=data)

    def response(self, data, error_status_code=status.HTTP_400_BAD_REQUEST):
        self._close_postgres_session()

        if self.errors:
            self._raise_exception(error_status_code=error_status_code)
        else:
            return {
                "data": data,
                "errors": self.errors
            }

    def response_paging(
            self,
            data,
            total_items: int = 1,
            current_page: int = 1,
            total_page: int = 1,
            error_status_code=status.HTTP_400_BAD_REQUEST
    ):
        self._close_postgres_session()

        if self.errors:
            self._raise_exception(error_status_code=error_status_code)
        else:
            return {
                "data": data,
                "total_items": total_items,
                "total_page": total_page,
                "current_page": current_page,
                "errors": self.errors,
            }

    def nested_list(
            self,
            objects: Union[dict, list],
            map_with_key: str,
            children_fields: dict,
            children_list: list = None,
            key_child_map_parent=None
    ):
        """
        thay kiểu dũ liệu trong childfields sẽ ra data như mong muốn
        - children_fields={"detail": {'t1', 't2'}}: data child la dict
        - children_fields={"detail": ['t1', 't2']}: data child la list
        - Có thể nest con vào cha theo trường hợp trên:
            + tách key mapping
        re = ctr.nested_list(objects=data, map_with_key='the_luong_id', children_fields={"detail": ['t1', 't2']})

        re = ctr.nested_list(
            objects=re, map_with_key='id', children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']}
        )

        re = ctr.nested_list(
            objects=NEST_PARENT_FD,
            map_with_key='id',
            children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']},
            children_list=NEST_CHILDREN_FD
        )
        """
        objects_cp = objects.copy()

        if isinstance(objects, dict):
            object_list = [objects_cp]
        else:
            object_list = objects_cp

        if not isinstance(children_fields, dict):
            raise Exception('fields type is dict')

        if len(children_fields) < 1:
            return objects_cp

        if not objects_cp:
            return objects_cp

        for key in children_fields:
            assert isinstance(children_fields[key], (list, set)), 'children is type list'
            assert len(children_fields[key]) > 0, 'children is not null'
            # assert children_fields[key][0][-2:] == "id", "First field of child  must be primary key ID"

        if children_list:
            data_result = self._nest_child_to_parent(
                parent_list=object_list,
                map_with_key=map_with_key,
                children_fields=children_fields,
                children_list=children_list,
                key_child_map_parent=key_child_map_parent
            )
        else:
            data_result = self._nest_me(
                objects=object_list,
                map_with_key=map_with_key,
                fields=children_fields
            )
        if isinstance(objects, dict):
            return data_result[0] if data_result else {}
        else:
            return data_result

    def _nest_me(
            self,
            objects: list,
            map_with_key: str,
            fields: dict
    ):

        all_key_child = []
        for key_child, value_child in fields.items():
            all_key_child += list(value_child)

        nest_level_data = list(
            map(
                lambda x: self._nest_level(data_item=x, all_key_child=all_key_child, fields=fields),
                objects
            )
        )

        key_in_parent = set()
        data_parent = dict()

        for temp in list(nest_level_data):
            if temp[map_with_key] not in key_in_parent:
                key_in_parent.add(temp[map_with_key])
                data_parent.update({
                    temp[map_with_key]: temp
                })
            else:
                for key_field, value_field in fields.items():
                    if not temp[key_field]:
                        continue

                    if isinstance(value_field, list):
                        if temp[key_field][0] not in data_parent[temp[map_with_key]][key_field]:
                            data_parent[temp[map_with_key]][key_field].append(temp[key_field][0])
        return list(data_parent.values())

    def _nest_child_to_parent(
            self, parent_list, map_with_key: str, children_fields: dict,
            children_list: list = None, key_child_map_parent=None
    ):

        all_key_child = []
        for key_child, value_child in children_fields.items():
            all_key_child += list(value_child)

        nest_level_data = list(
            map(
                lambda x: self._nest_level(data_item=x, all_key_child=all_key_child, fields=children_fields),
                children_list
            )
        )

        for parent in parent_list:
            for child in nest_level_data:
                if key_child_map_parent:
                    if parent[map_with_key] == child[key_child_map_parent]:
                        self._nest_type(parent=parent, child=child, children_fields=children_fields)
                else:
                    if parent[map_with_key] == child[map_with_key]:
                        self._nest_type(parent=parent, child=child, children_fields=children_fields)
        return parent_list

    @staticmethod
    def _nest_type(parent, child, children_fields):
        for key_field, value_field in children_fields.items():
            if not child[key_field]:
                continue
            if isinstance(value_field, list):
                if key_field not in parent:
                    parent.update({
                        key_field: [child[key_field][0]]
                    })
                elif child[key_field][0] not in parent[key_field]:
                    parent[key_field].append(child[key_field][0])
            else:
                parent.update({
                    key_field: child[key_field][0]
                })

    @staticmethod
    def _nest_level(data_item: dict, all_key_child: list, fields: dict):
        child_temp = {}
        parent_temp = {}
        for key_temp, value_temp in data_item.items():
            if key_temp in all_key_child:
                for key_field, value_field in fields.items():
                    if key_temp in value_field:
                        if key_field not in child_temp:
                            child_temp.update({
                                key_field: {}
                            })
                        child_temp[key_field].update({
                            key_temp: value_temp
                        })
            else:
                parent_temp.update({
                    key_temp: value_temp
                })

        for key_field, value_field in fields.items():
            if isinstance(value_field, list):
                parent_temp.update({
                    key_field: [child_temp[key_field]]
                })
            else:
                parent_temp.update({
                    key_field: child_temp[key_field]
                })

        return parent_temp

    @staticmethod
    def make_history_log_data(description: str, history_status: int, current_user: UserInfoResponse):
        history_log_data = [dict(
            description=description,
            completed_at=datetime_to_string(now()),
            created_at=datetime_to_string(now()),
            status=history_status,
            # Todo
            # data ghi log kafka.
        )]
        return history_log_data

    async def validate_issued_date(self, issued_date: date, loc: str):
        if issued_date > today():
            return self.response_exception(msg=ERROR_ISSUED_DATE, loc=loc)
        return issued_date

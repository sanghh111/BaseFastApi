from typing import Callable

from fastapi import FastAPI
from loguru import logger

# todo sử dụng khối này nếu đã config db
# Init Service Example
# from app.settings.service import SERVICE


# INIT_SERVICE = SERVICE


# todo xóa dòng này nếu đã config db
INIT_SERVICE = None


def create_start_app_handler(app: FastAPI) -> Callable:  # noqa
    async def start_app():
        # todo ví dụ chạy hàm khởi tạo
        
        
        pass
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # noqa
    @logger.catch
    async def stop_app() -> None:
        # todo ví dụ dừng hàm khởi tạo
        
        
        pass
    return stop_app

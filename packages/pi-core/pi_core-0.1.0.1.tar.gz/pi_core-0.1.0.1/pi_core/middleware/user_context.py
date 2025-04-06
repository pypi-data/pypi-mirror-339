from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Request
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class UserContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Replace with real logic (parse token/session)
        request.state.user_id = 42
        request.state.role = UserRole.teacher
        response = await call_next(request)
        return response
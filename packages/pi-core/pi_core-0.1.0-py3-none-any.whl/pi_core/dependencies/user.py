from fastapi import Request, Depends
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class UserContext:
    def __init__(
        self,
        user_id: int,
        role: UserRole,
        school_id: Optional[int] = None,
        org_id: Optional[int] = None,
    ):
        self.user_id = user_id
        self.role = role
        self.school_id = school_id
        self.org_id = org_id


def get_current_user(request: Request) -> UserContext:
    """
    Extracts the user context from the request set by middleware.
    Works across all apps that use UserContextMiddleware or its subclasses.
    """
    if not hasattr(request.state, "user_id") or not hasattr(request.state, "role"):
        raise RuntimeError("User context not set. Is the middleware installed?")
    
    return UserContext(
        user_id=request.state.user_id,
        role=request.state.role,
        school_id=getattr(request.state, "school_id", None),
        org_id=getattr(request.state, "org_id", None),
    )
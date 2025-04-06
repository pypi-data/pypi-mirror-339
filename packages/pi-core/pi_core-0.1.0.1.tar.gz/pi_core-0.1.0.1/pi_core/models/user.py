from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum
from pydantic import field_validator
from pi_core.utils.validators import validate_email_domain


class UserRole(str, Enum):
    TEACHER = "teacher"
    STAFF = "staff"
    SCHOOL_ADMIN = "school-admin"
    STUDENT = "student"

class User(BaseModel):
    """Public-safe user schema intended for API responses and internal sharing.
    
    This model intentionally excludes sensitive data such as passwords, tokens,
    or authentication credentials.
    """
    id: int
    email: EmailStr = Field(..., description="User's verified institutional email", repr=False)
    roles: List[UserRole]

    @field_validator("email")
    def restrict_email_domain(cls, value):
        return validate_email_domain(value)
    class Config:
        extra = "forbid"  # Prevent unwanted fields from being added
        orm_mode = True   # Allow loading from ORM objects
        json_encoders = {
            EmailStr: lambda v: v.lower()
        }

    def __init__(self, **data):
        if "email" in data:
            data["email"] = data["email"].lower()
        super().__init__(**data)

class UserPrivate(User):
    """Sensitive user model used only internally. Not exposed via public APIs."""
    hashed_password: str = Field(..., description="Hashed user password", repr=False)
    is_active: bool = Field(default=True, description="Whether the user account is active")
    last_login: str | None = Field(default=None, description="Timestamp of last login")

class UserPublic(BaseModel):
    """Public-facing user model for listings and directory views.
    
    Safe for exposure to students, staff directories, or dashboards.
    """
    id: int
    display_name: Optional[str] = Field(default=None, description="Short name or initials for public display")
    roles: List[UserRole]
    school_id: Optional[int] = Field(default=None, description="School the user is associated with")

    class Config:
        extra = "forbid"
        orm_mode = True
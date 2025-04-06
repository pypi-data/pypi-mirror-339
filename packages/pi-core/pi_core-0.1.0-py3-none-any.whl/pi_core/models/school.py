from pydantic import BaseModel, Field
from typing import Optional

class School(BaseModel):
    """Internal school model shared across PI services for full CRUD and linking."""
    id: int
    name: str = Field(..., description="Official school name")
    domain: str = Field(..., description="Unique subdomain used for school login (e.g. myschool.pi.edu)")
    country: Optional[str] = Field(default=None, description="Country where the school is located")
    is_active: bool = Field(default=True, description="Whether the school is operational")
    created_by: Optional[int] = Field(default=None, description="ID of the user who created this school record")

    class Config:
        extra = "forbid"
        orm_mode = True


class SchoolPublic(BaseModel):
    """Public-facing school model for safe display in directories or external APIs."""
    id: int
    name: str = Field(..., description="Display name of the school")
    domain: str = Field(..., description="Public subdomain")
    country: Optional[str] = Field(default=None, description="Country (if shown publicly)")

    class Config:
        extra = "forbid"
        orm_mode = True
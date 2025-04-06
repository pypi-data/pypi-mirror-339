from pydantic import BaseModel, Field, field_validator
from typing import Optional
from pi_core.utils.validators import validate_domain



class SchoolPublic(BaseModel):
    """
    Public-facing school model for open APIs, listings, or unauthenticated views.
    Contains non-sensitive fields only.
    """

    id: int
    name: str = Field(..., description="Display name of the school")
    domain: str = Field(..., description="Public subdomain")
    country: Optional[str] = Field(default=None, description="Country (if shown publicly)")

    class Config:
        extra = "forbid"
        orm_mode = True
        from_attributes = True


class School(BaseModel):
    """Internal school model shared across PI services for full CRUD and linking."""
    id: int
    name: str = Field(..., description="Official school name")
    domain: str = Field(..., description="Unique subdomain used for school login (e.g. myschool.pi.edu)")
    country: Optional[str] = Field(default=None, description="Country where the school is located")
    is_active: bool = Field(default=True, description="Whether the school is operational")
    created_by: Optional[int] = Field(default=None, description="ID of the user who created this school record")

    @field_validator("domain")
    def enforce_school_domain(cls, value):
        return validate_domain(value)
    
    class Config:
        extra = "forbid"
        orm_mode = True

    def to_public(self) -> SchoolPublic:
        """
        Converts this internal School object into a public-safe `SchoolPublic` model.
        Returns:
            SchoolPublic: A redacted, safe version suitable for open API exposure.
        """
        return SchoolPublic(
            id=self.id,
            name=self.name,
            domain=self.domain,
            country=self.country
        )
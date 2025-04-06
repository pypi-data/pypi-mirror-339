from pydantic import BaseModel, Field
from typing import Optional
from datetime import date



def to_admin_dict(self) -> dict:
    """Returns a dictionary containing only fields marked as admin-only."""
    return {
        k: v for k, v in self.dict()
        if self.__fields__[k].field_info.extra.get("admin_only", False)
    }
# This function is used to redact sensitive fields from the model
# when creating a public representation of the model.
def redact_admin_fields(model: BaseModel) -> dict:
    return {
        k: v for k, v in model.dict()
        if not model.__fields__[k].field_info.extra.get("admin_only", False)
    }

def to_redacted_dict(self) -> dict:
    """Returns a dictionary excluding admin-only fields based on metadata."""
    return {
        k: v for k, v in self.dict()
        if not self.__fields__[k].field_info.extra.get("admin_only", False)
    }

class PupilPublic(BaseModel):
    """Safe, read-only representation of a pupil for use in public listings or dashboards."""
    id: int
    full_name: str = Field(..., description="Pupil's full display name")
    year_group: str = Field(..., description="Academic year or class grouping")
    enrolled: bool = Field(..., description="Enrolment status")

    class Config:
        extra = "forbid"
        orm_mode = True

    @classmethod
    def from_private(cls, pupil: "Pupil") -> "PupilPublic":
        return cls(id=pupil.id, full_name=pupil.full_name, year_group=pupil.year_group, enrolled=pupil.enrolled)


class Pupil(BaseModel):
    """Internal model representing a pupil record used for attendance, academic tracking, and school linkage."""
    id: int
    full_name: str = Field(..., description="Full legal name of the pupil")
    year_group: str = Field(..., description="Academic year group or class")
    enrolled: bool = Field(default=True, description="Whether the pupil is currently enrolled")
    school_id: Optional[int] = Field(default=None, description="Associated school ID")
    guardian_contact: Optional[str] = Field(default=None, description="Parent or guardian contact info", repr=False)
    notes: Optional[str] = Field(default=None, description="Additional internal notes (not public)", repr=False)

    class Config:
        extra = "forbid"
        orm_mode = True

    def to_public(self) -> PupilPublic:
        return PupilPublic.from_private(self)


from typing import Annotated

class PupilPrivate(Pupil):
    """Internal-use pupil model containing sensitive or extended information."""
    date_of_birth: Annotated[Optional[date], Field(default=None, description="DOB", metadata={"admin_only": True})]
    medical_notes: Annotated[Optional[str], Field(default=None, description="Medical info", metadata={"admin_only": True})]
    safeguarding_flags: Annotated[Optional[bool], Field(default=False, description="Safeguarding", metadata={"admin_only": True})]
    behaviour_notes: Annotated[Optional[str], Field(default=None, description="Behavioural notes", metadata={"admin_only": True})]

    class Config:
        extra = "forbid"
        orm_mode = True

    def to_public(self) -> PupilPublic:
        return super().to_public()
    
    def to_dict_by_role(self, role: str) -> dict:
        """Return pupil data based on role access level."""
        if role == "admin":
            return self.dict()
        return self.to_redacted_dict()
    
class PupilLite(BaseModel):
    """Minimal read-only representation of a pupil, suitable for dropdowns and attendance use."""
    id: int
    full_name: str = Field(..., description="Full name for identification")

    class Config:
        extra = "forbid"
        orm_mode = True
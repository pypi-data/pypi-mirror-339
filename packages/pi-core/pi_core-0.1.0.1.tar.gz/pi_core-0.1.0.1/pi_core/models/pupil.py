from pydantic import BaseModel, Field, field_validator
from pi_core.utils.validators import validate_dob
from typing import Optional, TypeVar
from datetime import date
from typing import Annotated

ModelType = TypeVar("ModelType", bound=BaseModel)

def _is_admin_only_field(field_info):
    return field_info.metadata.get("admin_only", False)

class BaseModelWithAdminControl(BaseModel):
    """Base model providing admin control features for Pydantic models."""
    
    def to_admin_dict(self) -> dict:
        """Return a dictionary with only admin-only fields."""
        return {
            k: v for k, v in self.model_dump().items()
            if self.model_fields[k].field_info.metadata.get("admin_only", False)
        }

    def to_redacted_dict(self) -> dict:
        """Return a dictionary excluding admin-only fields."""
        return {
            k: v for k, v in self.model_dump().items()
            if not self.model_fields[k].field_info.metadata.get("admin_only", False)
        }

class PupilPublic(BaseModelWithAdminControl):
    """Read-only representation of a pupil for public use."""
    id: int
    full_name: str = Field(..., description="Pupil's full display name")
    year_group: str = Field(..., description="Academic year or class grouping")
    enrolled: bool = Field(..., description="Enrolment status")

    class Config:
        extra = "forbid"
        orm_mode = True

    @classmethod
    def from_private(cls, pupil: "Pupil") -> "PupilPublic":
        """Create a PupilPublic instance from a Pupil instance."""
        return cls(id=pupil.id, full_name=pupil.full_name, year_group=pupil.year_group, enrolled=pupil.enrolled)

class Pupil(BaseModelWithAdminControl):
    """Model representing a pupil record for internal use."""
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
        """Convert the Pupil instance to its public representation."""
        return PupilPublic.from_private(self)

class PupilPrivate(Pupil):
    """Internal-use pupil model containing sensitive information."""
    date_of_birth: Annotated[Optional[date], Field(default=None, description="DOB", metadata={"admin_only": True})]
    medical_notes: Annotated[Optional[str], Field(default=None, description="Medical info", metadata={"admin_only": True})]
    safeguarding_flags: Annotated[Optional[bool], Field(default=False, description="Safeguarding", metadata={"admin_only": True})]
    behaviour_notes: Annotated[Optional[str], Field(default=None, description="Behavioural notes", metadata={"admin_only": True})]

    class Config:
        extra = "forbid"
        orm_mode = True

    @field_validator("date_of_birth")
    def dob_cannot_be_future(cls, value):
        """Ensure the date of birth is not in the future."""
        return validate_dob(value)

    def to_public(self) -> PupilPublic:
        """Convert the PupilPrivate instance to its public representation."""
        return super().to_public()

    def to_dict_by_role(self, role: str) -> dict:
        """Return pupil data based on role."""
        role_actions = {
            "admin": self.model_dump,
            "public": self.to_redacted_dict,
            "teacher": self.to_redacted_dict,  # Assuming teachers see the same as public
        }
        action = role_actions.get(role, self.to_redacted_dict)  # Default to redacted
        return action()

class PupilLite(BaseModelWithAdminControl):
    """Minimal representation of a pupil for lightweight use."""
    id: int
    full_name: str = Field(..., description="Full name for identification")

    def to_lite(self) -> "PupilLite":
        """Convert the Pupil instance to a lightweight representation."""
        return PupilLite(id=self.id, full_name=self.full_name)

    class Config:
        extra = "forbid"
        orm_mode = True
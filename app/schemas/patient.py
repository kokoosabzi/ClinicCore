from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    national_code: str | None = Field(default=None, max_length=10)
    phone: str | None = Field(default=None, max_length=20)
    notes: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

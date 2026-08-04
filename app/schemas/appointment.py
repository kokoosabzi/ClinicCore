from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    patient_id: int
    starts_at: datetime
    reason: str | None = Field(default=None, max_length=200)
    notes: str | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    id: int
    status: AppointmentStatus
    model_config = ConfigDict(from_attributes=True)

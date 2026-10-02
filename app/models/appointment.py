from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class AppointmentStatus(StrEnum):
    booked = "booked"
    rescheduled = "rescheduled"
    cancelled = "cancelled"
    waiting = "waiting"
    no_show = "no_show"
    completed = "completed"


class Appointment(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(String(200))
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.booked, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    patient = relationship("Patient", back_populates="appointments")

    __table_args__ = (
        # ClinicCore currently schedules a single shared appointment slot.
        # Deleted appointments do not occupy a slot and can be replaced.
        Index(
            "uq_active_appointment_starts_at",
            "starts_at",
            unique=True,
            postgresql_where=text("NOT is_deleted"),
            sqlite_where=text("is_deleted = 0"),
        ),
    )

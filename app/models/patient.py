from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class Patient(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    national_code: Mapped[str | None] = mapped_column(String(10), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), index=True)
    notes: Mapped[str | None] = mapped_column(Text)

    appointments = relationship("Appointment", back_populates="patient")

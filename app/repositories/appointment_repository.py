from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment


class AppointmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Appointment]:
        return list(self.db.scalars(select(Appointment).where(Appointment.is_deleted.is_(False)).order_by(Appointment.starts_at)))

    def has_active_slot(self, starts_at: datetime) -> bool:
        statement = select(Appointment.id).where(
            Appointment.starts_at == starts_at,
            Appointment.is_deleted.is_(False),
        )
        return self.db.scalar(statement) is not None

    def create(self, appointment: Appointment) -> Appointment:
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

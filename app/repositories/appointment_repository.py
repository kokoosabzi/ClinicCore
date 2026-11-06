from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.audit import AuditLog


class AppointmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Appointment]:
        return list(self.db.scalars(
            select(Appointment)
            .where(Appointment.is_deleted.is_(False))
            .order_by(Appointment.starts_at.desc())
        ))

    def get(self, appointment_id: int) -> Appointment | None:
        return self.db.scalar(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.is_deleted.is_(False),
            )
        )

    def has_active_slot(self, starts_at: datetime, exclude_id: int | None = None) -> bool:
        statement = select(Appointment.id).where(
            Appointment.starts_at == starts_at,
            Appointment.is_deleted.is_(False),
            Appointment.status != "cancelled",
        )
        if exclude_id is not None:
            statement = statement.where(Appointment.id != exclude_id)
        return self.db.scalar(statement) is not None

    def create(self, appointment: Appointment) -> Appointment:
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def save_change(self, appointment: Appointment, event: AuditLog) -> Appointment:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

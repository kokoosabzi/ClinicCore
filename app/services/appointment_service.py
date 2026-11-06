import json

from sqlalchemy.exc import IntegrityError

from app.models.appointment import Appointment, AppointmentStatus
from app.models.audit import AuditLog
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import AppointmentCreate


class AppointmentSlotUnavailableError(ValueError):
    """Raised when an active appointment already occupies a shared time slot."""


class AppointmentNotFoundError(ValueError):
    """Raised when an appointment cannot be found or is archived."""


class InvalidAppointmentTransitionError(ValueError):
    """Raised when a requested appointment state transition is not allowed."""


_ALLOWED_TRANSITIONS = {
    AppointmentStatus.booked: {
        AppointmentStatus.waiting,
        AppointmentStatus.cancelled,
        AppointmentStatus.no_show,
        AppointmentStatus.completed,
    },
    AppointmentStatus.rescheduled: {
        AppointmentStatus.waiting,
        AppointmentStatus.cancelled,
        AppointmentStatus.no_show,
        AppointmentStatus.completed,
    },
    AppointmentStatus.waiting: {
        AppointmentStatus.completed,
        AppointmentStatus.no_show,
        AppointmentStatus.cancelled,
    },
    AppointmentStatus.cancelled: set(),
    AppointmentStatus.no_show: set(),
    AppointmentStatus.completed: set(),
}


class AppointmentService:
    def __init__(self, repository: AppointmentRepository) -> None:
        self.repository = repository

    def list_appointments(self) -> list[Appointment]:
        return self.repository.list()

    def book(self, data: AppointmentCreate) -> Appointment:
        if self.repository.has_active_slot(data.starts_at):
            raise AppointmentSlotUnavailableError("Appointment time is already booked")
        try:
            return self.repository.create(Appointment(**data.model_dump()))
        except IntegrityError as error:
            self.repository.db.rollback()
            message = str(error.orig)
            if "uq_active_appointment_starts_at" in message or "appointments.starts_at" in message:
                raise AppointmentSlotUnavailableError("Appointment time is already booked") from error
            raise

    def change_status(
        self,
        appointment_id: int,
        new_status: AppointmentStatus,
        *,
        actor: str | None,
    ) -> Appointment:
        appointment = self.repository.get(appointment_id)
        if appointment is None:
            raise AppointmentNotFoundError("نوبت موردنظر پیدا نشد.")
        allowed = _ALLOWED_TRANSITIONS.get(appointment.status, set())
        if new_status not in allowed:
            raise InvalidAppointmentTransitionError(
                f"تغییر وضعیت از «{appointment.status.value}» به «{new_status.value}» مجاز نیست."
            )
        previous_status = appointment.status
        appointment.status = new_status
        event = AuditLog(
            actor=actor,
            action="appointment.status_changed",
            entity="appointment",
            entity_id=str(appointment.id),
            details=json.dumps(
                {"from": previous_status.value, "to": new_status.value},
                ensure_ascii=False,
            ),
        )
        return self.repository.save_change(appointment, event)

    def reschedule(
        self,
        appointment_id: int,
        starts_at,
        *,
        actor: str | None,
    ) -> Appointment:
        appointment = self.repository.get(appointment_id)
        if appointment is None:
            raise AppointmentNotFoundError("نوبت موردنظر پیدا نشد.")
        if appointment.status not in {AppointmentStatus.booked, AppointmentStatus.rescheduled}:
            raise InvalidAppointmentTransitionError("فقط نوبت ثبت‌شده یا تغییرزمان‌یافته قابل جابه‌جایی است.")
        if appointment.starts_at == starts_at:
            raise InvalidAppointmentTransitionError("زمان جدید با زمان فعلی یکسان است.")
        if self.repository.has_active_slot(starts_at, exclude_id=appointment.id):
            raise AppointmentSlotUnavailableError("Appointment time is already booked")
        previous_time = appointment.starts_at.isoformat(timespec="minutes")
        appointment.starts_at = starts_at
        appointment.status = AppointmentStatus.rescheduled
        event = AuditLog(
            actor=actor,
            action="appointment.rescheduled",
            entity="appointment",
            entity_id=str(appointment.id),
            details=json.dumps(
                {"from": previous_time, "to": starts_at.isoformat(timespec="minutes")},
                ensure_ascii=False,
            ),
        )
        try:
            return self.repository.save_change(appointment, event)
        except IntegrityError as error:
            self.repository.db.rollback()
            message = str(error.orig)
            if "uq_active_appointment_starts_at" in message or "appointments.starts_at" in message:
                raise AppointmentSlotUnavailableError("Appointment time is already booked") from error
            raise

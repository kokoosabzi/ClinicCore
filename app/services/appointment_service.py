from sqlalchemy.exc import IntegrityError

from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import AppointmentCreate


class AppointmentSlotUnavailableError(ValueError):
    """Raised when an active appointment already occupies a shared time slot."""


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
            # The partial unique index is the final guard when two requests
            # pass the pre-check concurrently.  Roll back before translating
            # the database constraint into the domain-level result.
            self.repository.db.rollback()
            message = str(error.orig)
            if "uq_active_appointment_starts_at" in message or "appointments.starts_at" in message:
                raise AppointmentSlotUnavailableError("Appointment time is already booked") from error
            raise

from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import AppointmentCreate


class AppointmentService:
    def __init__(self, repository: AppointmentRepository) -> None:
        self.repository = repository

    def list_appointments(self) -> list[Appointment]:
        return self.repository.list()

    def book(self, data: AppointmentCreate) -> Appointment:
        return self.repository.create(Appointment(**data.model_dump()))

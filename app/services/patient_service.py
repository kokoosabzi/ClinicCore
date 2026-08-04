from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate


class PatientService:
    def __init__(self, repository: PatientRepository) -> None:
        self.repository = repository

    def list_patients(self, search: str | None = None) -> list[Patient]:
        return self.repository.list(search=search)

    def get_patient(self, patient_id: int) -> Patient | None:
        return self.repository.get(patient_id)

    def create_patient(self, data: PatientCreate) -> Patient:
        return self.repository.create(Patient(**data.model_dump()))

    def update_patient(self, patient: Patient, data: PatientCreate) -> Patient:
        return self.repository.update(patient, data.model_dump())

    def delete_patient(self, patient: Patient) -> None:
        self.repository.soft_delete(patient)

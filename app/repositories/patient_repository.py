from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.patient import Patient


class PatientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, search: str | None = None) -> list[Patient]:
        statement = select(Patient).where(Patient.is_deleted.is_(False)).order_by(Patient.id.desc())
        if search:
            term = f"%{search}%"
            statement = statement.where(
                or_(Patient.first_name.ilike(term), Patient.last_name.ilike(term), Patient.phone.ilike(term), Patient.national_code.ilike(term))
            )
        return list(self.db.scalars(statement))

    def get(self, patient_id: int) -> Patient | None:
        return self.db.scalar(select(Patient).where(Patient.id == patient_id, Patient.is_deleted.is_(False)))

    def create(self, patient: Patient) -> Patient:
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def update(self, patient: Patient, data: dict[str, object]) -> Patient:
        for key, value in data.items():
            setattr(patient, key, value)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def soft_delete(self, patient: Patient) -> None:
        patient.is_deleted = True
        self.db.commit()

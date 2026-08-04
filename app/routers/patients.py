from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_user
from app.core.database import get_db
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientRead
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


def get_service(db: Session = Depends(get_db)) -> PatientService:
    return PatientService(PatientRepository(db))


@router.get("/", response_model=list[PatientRead])
def list_patients(user=Depends(require_user), service: PatientService = Depends(get_service)):
    return service.list_patients()


@router.post("/", response_model=PatientRead, status_code=201)
def create_patient(payload: PatientCreate, user=Depends(require_user), service: PatientService = Depends(get_service)):
    return service.create_patient(payload)

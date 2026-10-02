from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import require_user
from app.core.database import get_db
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import AppointmentCreate, AppointmentRead
from app.services.appointment_service import AppointmentService, AppointmentSlotUnavailableError

router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_service(db: Session = Depends(get_db)) -> AppointmentService:
    return AppointmentService(AppointmentRepository(db))


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(user=Depends(require_user), service: AppointmentService = Depends(get_service)):
    return service.list_appointments()


@router.post("/", response_model=AppointmentRead, status_code=201)
def book_appointment(payload: AppointmentCreate, user=Depends(require_user), service: AppointmentService = Depends(get_service)):
    try:
        return service.book(payload)
    except AppointmentSlotUnavailableError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error

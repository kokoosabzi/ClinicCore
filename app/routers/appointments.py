from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import require_permission
from app.core.database import get_db
from app.models.appointment import AppointmentStatus
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentReschedule,
    AppointmentStatusUpdate,
)
from app.services.appointment_service import (
    AppointmentNotFoundError,
    AppointmentService,
    AppointmentSlotUnavailableError,
    InvalidAppointmentTransitionError,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_service(db: Session = Depends(get_db)) -> AppointmentService:
    return AppointmentService(AppointmentRepository(db))


def _raise_domain_error(error: ValueError) -> None:
    if isinstance(error, AppointmentNotFoundError):
        raise HTTPException(status_code=404, detail=str(error)) from error
    if isinstance(error, AppointmentSlotUnavailableError):
        raise HTTPException(status_code=409, detail=str(error)) from error
    if isinstance(error, InvalidAppointmentTransitionError):
        raise HTTPException(status_code=422, detail=str(error)) from error
    raise error


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(user=Depends(require_permission("appointments.view")), service: AppointmentService = Depends(get_service)):
    return service.list_appointments()


@router.post("/", response_model=AppointmentRead, status_code=201)
def book_appointment(payload: AppointmentCreate, user=Depends(require_permission("appointments.create")), service: AppointmentService = Depends(get_service)):
    try:
        return service.book(payload)
    except AppointmentSlotUnavailableError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
def update_appointment_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    user=Depends(require_permission("appointments.update")),
    service: AppointmentService = Depends(get_service),
):
    if payload.status == AppointmentStatus.cancelled:
        raise HTTPException(status_code=403, detail="Use the cancellation action and permission.")
    try:
        return service.change_status(appointment_id, payload.status, actor=str(user["username"]))
    except ValueError as error:
        _raise_domain_error(error)


@router.post("/{appointment_id}/cancel", response_model=AppointmentRead)
def cancel_appointment(
    appointment_id: int,
    user=Depends(require_permission("appointments.cancel")),
    service: AppointmentService = Depends(get_service),
):
    try:
        return service.change_status(appointment_id, AppointmentStatus.cancelled, actor=str(user["username"]))
    except ValueError as error:
        _raise_domain_error(error)


@router.patch("/{appointment_id}/reschedule", response_model=AppointmentRead)
def reschedule_appointment(
    appointment_id: int,
    payload: AppointmentReschedule,
    user=Depends(require_permission("appointments.update")),
    service: AppointmentService = Depends(get_service),
):
    try:
        return service.reschedule(appointment_id, payload.starts_at, actor=str(user["username"]))
    except ValueError as error:
        _raise_domain_error(error)

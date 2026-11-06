from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import require_permission
from app.core.database import get_db
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserResetPasswordResult, UserUpdate
from app.services.user_service import UserManagementError, UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.get("/", response_model=list[UserRead])
def list_users(
    user=Depends(require_permission("users.view")),
    service: UserService = Depends(get_service),
):
    return service.list_users()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    user=Depends(require_permission("users.create")),
    service: UserService = Depends(get_service),
):
    if payload.role == UserRole.admin and user["role"] != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Only a system administrator can create an administrator")
    try:
        return service.create_user(payload)
    except UserManagementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    user=Depends(require_permission("users.update")),
    service: UserService = Depends(get_service),
):
    if payload.role != UserRole(user["role"]) and "users.assign_role" not in user.get("permissions", []):
        raise HTTPException(status_code=403, detail="Role assignment is not permitted")
    try:
        return service.update_user(user_id, payload, actor_role=UserRole(user["role"]))
    except UserManagementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/{user_id}/deactivate", response_model=UserRead)
def deactivate_user(
    user_id: int,
    user=Depends(require_permission("users.deactivate")),
    service: UserService = Depends(get_service),
):
    try:
        return service.set_active(user_id, active=False, actor_id=int(user["id"]))
    except UserManagementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/{user_id}/reactivate", response_model=UserRead)
def reactivate_user(
    user_id: int,
    user=Depends(require_permission("users.deactivate")),
    service: UserService = Depends(get_service),
):
    try:
        return service.set_active(user_id, active=True, actor_id=int(user["id"]))
    except UserManagementError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{user_id}/reset-password", response_model=UserResetPasswordResult)
def reset_password(
    user_id: int,
    user=Depends(require_permission("users.reset_password")),
    service: UserService = Depends(get_service),
):
    try:
        target, temporary_password = service.reset_password(user_id)
    except UserManagementError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return UserResetPasswordResult(user_id=target.id, temporary_password=temporary_password)

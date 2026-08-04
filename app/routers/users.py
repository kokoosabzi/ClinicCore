from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_admin
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.get("/", response_model=list[UserRead])
def list_users(user=Depends(require_admin), service: UserService = Depends(get_service)):
    return service.list_users()


@router.post("/", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, user=Depends(require_admin), service: UserService = Depends(get_service)):
    return service.create_user(payload)

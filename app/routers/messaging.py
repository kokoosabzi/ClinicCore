from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_admin, require_user
from app.core.database import get_db
from app.repositories.messaging_repository import MessageRepository
from app.schemas.messaging import MessageCreate, MessageRead
from app.services.messaging_service import MessagingService

router = APIRouter(prefix="/messages", tags=["messages"])


def get_service(db: Session = Depends(get_db)) -> MessagingService:
    return MessagingService(MessageRepository(db))


@router.get("/", response_model=list[MessageRead])
def list_messages(user=Depends(require_user), service: MessagingService = Depends(get_service)):
    return service.list_messages()


@router.post("/", response_model=MessageRead, status_code=201)
def queue_message(payload: MessageCreate, user=Depends(require_user), service: MessagingService = Depends(get_service)):
    return service.queue_message(payload)


@router.post("/send-pending")
def send_pending_messages(user=Depends(require_admin), service: MessagingService = Depends(get_service)):
    return {"sent": service.send_pending()}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_user
from app.core.database import get_db
from app.repositories.financial_repository import ExpenseRepository, PaymentRepository
from app.schemas.financial import ExpenseCreate, ExpenseRead, PaymentCreate, PaymentRead
from app.services.financial_service import FinancialService

router = APIRouter(prefix="/financial", tags=["financial"])


def get_service(db: Session = Depends(get_db)) -> FinancialService:
    return FinancialService(PaymentRepository(db), ExpenseRepository(db))


@router.get("/payments", response_model=list[PaymentRead])
def list_payments(user=Depends(require_user), service: FinancialService = Depends(get_service)):
    return service.list_payments()


@router.post("/payments", response_model=PaymentRead, status_code=201)
def record_payment(payload: PaymentCreate, user=Depends(require_user), service: FinancialService = Depends(get_service)):
    return service.record_payment(payload)


@router.get("/expenses", response_model=list[ExpenseRead])
def list_expenses(user=Depends(require_user), service: FinancialService = Depends(get_service)):
    return service.list_expenses()


@router.post("/expenses", response_model=ExpenseRead, status_code=201)
def record_expense(payload: ExpenseCreate, user=Depends(require_user), service: FinancialService = Depends(get_service)):
    return service.record_expense(payload)

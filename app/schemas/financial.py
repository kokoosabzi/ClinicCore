from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.financial import ExpenseCategory, PaymentStatus


class PaymentCreate(BaseModel):
    patient_id: int
    amount: int = Field(gt=0)
    paid_at: date
    status: PaymentStatus = PaymentStatus.paid
    description: str | None = None


class PaymentRead(PaymentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    amount: int = Field(gt=0)
    spent_at: date
    category: ExpenseCategory = ExpenseCategory.other
    description: str | None = None


class ExpenseRead(ExpenseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

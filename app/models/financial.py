from datetime import date
from enum import StrEnum

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class PaymentStatus(StrEnum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"


class ExpenseCategory(StrEnum):
    rent = "rent"
    salary = "salary"
    supplies = "supplies"
    utilities = "utilities"
    other = "other"


class Payment(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    paid_at: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.paid, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    patient = relationship("Patient")


class Expense(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    spent_at: Mapped[date] = mapped_column(Date, nullable=False)
    category: Mapped[ExpenseCategory] = mapped_column(Enum(ExpenseCategory), default=ExpenseCategory.other, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

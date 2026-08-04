from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.financial import Expense, Payment
from app.models.patient import Patient


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def summary(self) -> dict[str, int]:
        return {
            "patients": self.db.scalar(select(func.count(Patient.id)).where(Patient.is_deleted.is_(False))) or 0,
            "appointments": self.db.scalar(select(func.count(Appointment.id)).where(Appointment.is_deleted.is_(False))) or 0,
            "income": self.db.scalar(select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.is_deleted.is_(False))) or 0,
            "expenses": self.db.scalar(select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.is_deleted.is_(False))) or 0,
        }

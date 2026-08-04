from app.models.financial import Expense, Payment
from app.repositories.financial_repository import ExpenseRepository, PaymentRepository
from app.schemas.financial import ExpenseCreate, PaymentCreate


class FinancialService:
    def __init__(self, payments: PaymentRepository, expenses: ExpenseRepository) -> None:
        self.payments = payments
        self.expenses = expenses

    def list_payments(self) -> list[Payment]:
        return self.payments.list()

    def record_payment(self, data: PaymentCreate) -> Payment:
        return self.payments.create(Payment(**data.model_dump()))

    def list_expenses(self) -> list[Expense]:
        return self.expenses.list()

    def record_expense(self, data: ExpenseCreate) -> Expense:
        return self.expenses.create(Expense(**data.model_dump()))

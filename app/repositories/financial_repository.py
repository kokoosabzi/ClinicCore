from app.models.financial import Expense, Payment
from app.repositories.base import Repository


class PaymentRepository(Repository[Payment]):
    model = Payment


class ExpenseRepository(Repository[Expense]):
    model = Expense

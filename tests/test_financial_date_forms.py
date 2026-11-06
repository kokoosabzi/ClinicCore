import re
from datetime import date

from app.models.financial import Expense, Payment
from app.models.patient import Patient


def _csrf(client, path):
    response = client.get(path)
    assert response.status_code == 200
    token = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert token
    return response.text, token.group(1)


def test_financial_date_forms_render_jalali_picker(admin_client):
    for path, field in [
        ("/financial/payments/new", "paid_at"),
        ("/financial/expenses/new", "spent_at"),
    ]:
        html, _ = _csrf(admin_client, path)
        assert 'data-jalali-picker' in html
        assert 'data-jalali-value' in html
        assert f'name="{field}"' in html
        assert 'data-jalali-prev' in html
        assert 'data-jalali-next' in html


def test_payment_form_persists_gregorian_value_selected_from_jalali_picker(admin_client, db_session):
    patient = Patient(first_name="آزمایشی", last_name="بیمار")
    db_session.add(patient)
    db_session.commit()
    _, token = _csrf(admin_client, "/financial/payments/new")

    response = admin_client.post(
        "/ui/financial/payments",
        data={
            "csrf_token": token,
            "patient_id": str(patient.id),
            "amount": "250000",
            "paid_at": "2026-03-21",
            "description": "تست تاریخ جلالی",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    payment = db_session.query(Payment).filter_by(patient_id=patient.id).one()
    assert payment.paid_at == date(2026, 3, 21)


def test_expense_form_persists_gregorian_value_selected_from_jalali_picker(admin_client, db_session):
    _, token = _csrf(admin_client, "/financial/expenses/new")

    response = admin_client.post(
        "/ui/financial/expenses",
        data={
            "csrf_token": token,
            "title": "هزینه آزمایشی",
            "amount": "100000",
            "spent_at": "2026-03-21",
            "category": "other",
            "description": "تست تاریخ جلالی",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    expense = db_session.query(Expense).filter_by(title="هزینه آزمایشی").one()
    assert expense.spent_at == date(2026, 3, 21)

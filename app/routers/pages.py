from datetime import date, datetime
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import require_admin, require_user
from app.core.csrf import get_csrf_token, verify_csrf
from app.core.database import get_db
from app.models.appointment import Appointment
from app.models.financial import Expense, ExpenseCategory, Payment
from app.models.messaging import Message, MessageProvider
from app.models.patient import Patient
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.patient_repository import PatientRepository
from app.schemas.appointment import AppointmentCreate
from app.services.dashboard_service import DashboardService
from app.services.appointment_service import AppointmentService, AppointmentSlotUnavailableError
from app.services.patient_service import PatientService
from app.services.settings_service import SettingsService

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


def context(request: Request, title: str, **extra):
    return {
        "request": request,
        "title": title,
        "app_name": getattr(request.state, "app_name", "ClinicCore"),
        "app_title": getattr(request.state, "app_title", "ClinicCore"),
        "user": request.session.get("username"),
        "csrf_token": get_csrf_token(request),
        "app_theme": getattr(request.state, "app_theme", "system"),
        "app_density": getattr(request.state, "app_density", "comfortable"),
        **extra,
    }


def render(request: Request, template: str, title: str, **extra):
    return templates.TemplateResponse(
        request=request,
        name=template,
        context=context(request, title, **extra),
    )


async def form_data(request: Request) -> dict[str, str]:
    body = (await request.body()).decode("utf-8")
    return {key: values[-1] for key, values in parse_qs(body, keep_blank_values=True).items()}


def save_and_redirect(db: Session, entity, url: str = "/dashboard") -> RedirectResponse:
    db.add(entity)
    db.commit()
    return RedirectResponse(url=url, status_code=303)


def patient_payload(data: dict[str, str]) -> dict[str, str | None]:
    return {
        "first_name": data.get("first_name", "").strip(),
        "last_name": data.get("last_name", "").strip(),
        "national_code": data.get("national_code") or None,
        "phone": data.get("phone") or None,
        "notes": data.get("notes") or None,
    }


@router.get("/settings", response_class=HTMLResponse)
def settings_form(request: Request, db: Session = Depends(get_db), user=Depends(require_admin)):
    return render(
        request,
        "settings.html",
        "تنظیمات سامانه",
        settings=SettingsService(db).get_group("app") | SettingsService(db).get_group("clinic"),
        saved=request.query_params.get("saved") == "1",
    )


@router.post("/settings")
async def save_settings(request: Request, db: Session = Depends(get_db), user=Depends(require_admin)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    values = {
        "app.name": data.get("app_name", "").strip(),
        "app.title": data.get("app_title", "").strip(),
        "clinic.name": data.get("clinic_name", "").strip(),
        "clinic.address": data.get("clinic_address", "").strip(),
        "clinic.phone": data.get("clinic_phone", "").strip(),
        "clinic.email": data.get("clinic_email", "").strip(),
        "clinic.logo": data.get("clinic_logo", "").strip(),
        "clinic.header_text": data.get("clinic_header_text", "").strip(),
        "clinic.footer_text": data.get("clinic_footer_text", "").strip(),
    }
    if not values["app.name"] or not values["app.title"]:
        return render(
            request,
            "settings.html",
            "تنظیمات سامانه",
            settings=SettingsService(db).get_group("app") | SettingsService(db).get_group("clinic"),
            error="نام سامانه و عنوان نمایشی الزامی هستند.",
        )
    SettingsService(db).set_many(values)
    request.state.app_name = values["app.name"]
    request.state.app_title = values["app.title"]
    return RedirectResponse(url="/settings?saved=1", status_code=303)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    return render(request, "dashboard.html", "داشبورد", summary=DashboardService(db).summary())


@router.get("/patients", response_class=HTMLResponse)
def patients_index(request: Request, q: str | None = None, db: Session = Depends(get_db), user=Depends(require_user)):
    patients = PatientService(PatientRepository(db)).list_patients(search=q)
    return render(request, "patients/index.html", "بیماران", patients=patients, q=q or "")


@router.get("/patients/new", response_class=HTMLResponse)
def patient_form(request: Request, user=Depends(require_user)):
    return render(request, "patients/form.html", "ثبت بیمار", patient=None, action="/ui/patients")


@router.post("/ui/patients")
async def create_patient_from_form(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    patient = Patient(**patient_payload(data))
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return RedirectResponse(url=f"/patients/{patient.id}", status_code=303)


@router.get("/patients/{patient_id}", response_class=HTMLResponse)
def patient_detail(patient_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    patient = db.get(Patient, patient_id)
    if patient is None or patient.is_deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    appointments = list(db.scalars(select(Appointment).where(Appointment.patient_id == patient_id, Appointment.is_deleted.is_(False))))
    payments = list(db.scalars(select(Payment).where(Payment.patient_id == patient_id, Payment.is_deleted.is_(False))))
    return render(request, "patients/detail.html", "پرونده بیمار", patient=patient, appointments=appointments, payments=payments)


@router.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
def patient_edit(patient_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    patient = db.get(Patient, patient_id)
    if patient is None or patient.is_deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return render(request, "patients/form.html", "ویرایش بیمار", patient=patient, action=f"/ui/patients/{patient.id}")


@router.post("/ui/patients/{patient_id}")
async def update_patient_from_form(patient_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    patient = db.get(Patient, patient_id)
    if patient is None or patient.is_deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient_payload(data).items():
        setattr(patient, key, value)
    db.commit()
    return RedirectResponse(url=f"/patients/{patient.id}", status_code=303)


@router.post("/ui/patients/{patient_id}/delete")
async def delete_patient_from_form(patient_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_admin)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient.is_deleted = True
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)


@router.get("/appointments", response_class=HTMLResponse)
def appointments_index(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    appointments = list(db.scalars(select(Appointment).where(Appointment.is_deleted.is_(False)).order_by(Appointment.starts_at.desc())))
    return render(request, "appointments/index.html", "تقویم نوبت‌ها", appointments=appointments)


@router.get("/appointments/new", response_class=HTMLResponse)
def appointment_form(request: Request, user=Depends(require_user)):
    return render(request, "appointments/form.html", "ثبت نوبت")


@router.post("/ui/appointments")
async def create_appointment_from_form(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    appointment_data = AppointmentCreate(
        patient_id=int(data["patient_id"]),
        starts_at=datetime.fromisoformat(data["starts_at"]),
        reason=data.get("reason") or None,
        notes=data.get("notes") or None,
    )
    try:
        AppointmentService(AppointmentRepository(db)).book(appointment_data)
    except AppointmentSlotUnavailableError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return RedirectResponse(url="/appointments", status_code=303)


@router.get("/financial", response_class=HTMLResponse)
def financial_index(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    payments = list(db.scalars(select(Payment).where(Payment.is_deleted.is_(False)).order_by(Payment.paid_at.desc())))
    expenses = list(db.scalars(select(Expense).where(Expense.is_deleted.is_(False)).order_by(Expense.spent_at.desc())))
    return render(request, "financial/index.html", "مالی", payments=payments, expenses=expenses)


@router.get("/financial/payments/new", response_class=HTMLResponse)
def payment_form(request: Request, user=Depends(require_user)):
    return render(request, "financial/payment_form.html", "ثبت پرداخت")


@router.post("/ui/financial/payments")
async def create_payment_from_form(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    return save_and_redirect(
        db,
        Payment(patient_id=int(data["patient_id"]), amount=int(data["amount"]), paid_at=date.fromisoformat(data["paid_at"]), description=data.get("description") or None),
        "/financial",
    )


@router.get("/financial/expenses/new", response_class=HTMLResponse)
def expense_form(request: Request, user=Depends(require_user)):
    return render(request, "financial/expense_form.html", "ثبت هزینه")


@router.post("/ui/financial/expenses")
async def create_expense_from_form(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    return save_and_redirect(
        db,
        Expense(
            title=data.get("title", "").strip(),
            amount=int(data["amount"]),
            spent_at=date.fromisoformat(data["spent_at"]),
            category=ExpenseCategory(data.get("category") or ExpenseCategory.other),
            description=data.get("description") or None,
        ),
        "/financial",
    )


@router.get("/messages", response_class=HTMLResponse)
def messages_index(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    messages = list(db.scalars(select(Message).order_by(Message.id.desc())))
    return render(request, "messages/index.html", "پیام‌ها", messages=messages)


@router.get("/messages/new", response_class=HTMLResponse)
def message_form(request: Request, user=Depends(require_user)):
    return render(request, "messages/form.html", "ارسال پیام")


@router.post("/ui/messages")
async def create_message_from_form(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    return save_and_redirect(
        db,
        Message(recipient=data.get("recipient", "").strip(), provider=MessageProvider(data["provider"]), body=data.get("body", "").strip()),
        "/messages",
    )


@router.get("/print/patients/{patient_id}", response_class=HTMLResponse)
def print_patient(patient_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    patient = db.get(Patient, patient_id)
    return templates.TemplateResponse(
        request=request,
        name="print/patient_card.html",
        context=context(request, "چاپ پرونده بیمار", patient=patient),
    )


@router.get("/print/appointments/{appointment_id}", response_class=HTMLResponse)
def print_appointment(appointment_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    appointment = db.get(Appointment, appointment_id)
    return templates.TemplateResponse(
        request=request,
        name="print/appointment_receipt.html",
        context=context(request, "چاپ رسید نوبت", appointment=appointment),
    )


@router.get("/print/payments/{payment_id}", response_class=HTMLResponse)
def print_payment(payment_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    payment = db.get(Payment, payment_id)
    return templates.TemplateResponse(
        request=request,
        name="print/payment_receipt.html",
        context=context(request, "چاپ رسید پرداخت", payment=payment),
    )

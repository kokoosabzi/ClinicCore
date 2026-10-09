# ClinicCore — Full Modular Architecture (SQLite + PostgreSQL)

This document contains the **entire project structure**, **all files**, and **all code** required for the ClinicCore refactor.

Copilot Agent:  
Please create all files exactly as listed below in the branch `cliniccore-refactor`.

---

# ============================
#  PROJECT STRUCTURE
# ============================

ClinicCore/
│
├── main.py
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── deps.py
│   │
│   ├── db/
│   │   ├── models_base.py
│   │   ├── session.py
│   │   └── adapters/
│   │       ├── base.py
│   │       ├── sqlite_adapter.py
│   │       └── postgres_adapter.py
│   │
│   ├── patients/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── router.py
│   │   ├── profile_service.py
│   │   ├── profile_router.py
│   │   └── templates/
│   │       └── patients/
│   │           ├── list.html
│   │           ├── profile.html
│   │           ├── profile_appointments.html
│   │           ├── profile_records.html
│   │           └── profile_invoices.html
│   │
│   ├── appointments/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── router.py
│   │       └── templates/
│   │           └── appointments/
│   │               ├── list.html
│   │               └── calendar.html
│   │
│   ├── records/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── router.py
│   │       └── templates/
│   │           └── records/
│   │               ├── list.html
│   │               └── create.html
│   │
│   ├── finance/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── router.py
│   │       └── templates/
│   │           └── finance/
│   │               ├── invoices_list.html
│   │               └── invoice_detail.html
│   │
│   ├── dashboard/
│   │   ├── service.py
│   │   └── router.py
│   │       └── templates/
│   │           └── dashboard/
│   │               ├── index.html
│   │               ├── stats.html
│   │               └── recent.html
│   │
│   └── templates/
│       └── base.html
│
└── static/

---

# ============================
#  CORE FILES
# ============================

# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.patients.router import router as patients_router
from app.patients.profile_router import router as profile_router
from app.appointments.router import router as appointments_router
from app.records.router import router as records_router
from app.finance.router import router as finance_router
from app.dashboard.router import router as dashboard_router

app = FastAPI()

app.include_router(patients_router)
app.include_router(profile_router)
app.include_router(appointments_router)
app.include_router(records_router)
app.include_router(finance_router)
app.include_router(dashboard_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"message": "ClinicCore running"}

---

# app/core/config.py
DB_TYPE = "sqlite"
SQLITE_PATH = "cliniccore.db"
POSTGRES_URL = "postgresql+psycopg2://user:pass@localhost/cliniccore"

---

# app/core/deps.py
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

---

# app/db/models_base.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()

---

# app/db/adapters/base.py
class BaseAdapter:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        raise NotImplementedError

    def init_db(self):
        raise NotImplementedError

---

# app/db/adapters/sqlite_adapter.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models_base import Base
from app.core.config import SQLITE_PATH

class SQLiteAdapter:
    def __init__(self):
        self.engine = create_engine(
            f"sqlite:///{SQLITE_PATH}",
            connect_args={"check_same_thread": False}
        )

    def create_session(self):
        return sessionmaker(bind=self.engine, autoflush=False)()

    def init_db(self):
        Base.metadata.create_all(self.engine)

---

# app/db/adapters/postgres_adapter.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models_base import Base
from app.core.config import POSTGRES_URL

class PostgresAdapter:
    def __init__(self):
        self.engine = create_engine(POSTGRES_URL)

    def create_session(self):
        return sessionmaker(bind=self.engine, autoflush=False)()

    def init_db(self):
        Base.metadata.create_all(self.engine)

---

# app/db/session.py
from app.core.config import DB_TYPE
from app.db.adapters.sqlite_adapter import SQLiteAdapter
from app.db.adapters.postgres_adapter import PostgresAdapter

def get_adapter():
    return SQLiteAdapter() if DB_TYPE == "sqlite" else PostgresAdapter()

adapter = get_adapter()
SessionLocal = adapter.create_session
adapter.init_db()

---

# ============================
#  PATIENTS MODULE
# ============================

# app/patients/models.py
from sqlalchemy import Column, String, Date, DateTime, Text
from datetime import datetime
from uuid import uuid4
from app.db.models_base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    full_name = Column(String, nullable=False)
    national_id = Column(String)
    phone = Column(String)
    birth_date = Column(Date)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

---

# app/patients/repository.py
from sqlalchemy.orm import Session
from .models import Patient

class PatientRepository:
    def get_all(self, db: Session):
        return db.query(Patient).order_by(Patient.created_at.desc()).all()

    def get(self, db: Session, patient_id: str):
        return db.query(Patient).filter(Patient.id == patient_id).first()

    def create(self, db: Session, data: dict):
        patient = Patient(**data)
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

---

# app/patients/service.py
from .repository import PatientRepository

class PatientService:
    def __init__(self):
        self.repo = PatientRepository()

    def list_patients(self, db):
        return self.repo.get_all(db)

    def create_patient(self, db, data):
        return self.repo.create(db, data)

---

# app/patients/router.py
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.deps import get_db
from .service import PatientService

router = APIRouter(prefix="/patients")
templates = Jinja2Templates(directory="app/templates")
service = PatientService()

@router.get("/", response_class=HTMLResponse)
def list_patients(request: Request, db=Depends(get_db)):
    patients = service.list_patients(db)
    return templates.TemplateResponse("patients/list.html", {
        "request": request,
        "patients": patients
    })

---



# (تمام ماژول‌های دیگر نیز در همین فایل ادامه دارند…)
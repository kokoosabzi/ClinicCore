# AGENTS.md
# ClinicCore AI Development Rules

## Project Identity

Project Name:

ClinicCore

Purpose:

A lightweight, modular clinic management platform for small medical offices and healthcare centers.

Target users:

- Doctors
- Therapists
- Small clinics
- Medical offices
- Healthcare service providers

This project is NOT:

- Hospital Information System
- Enterprise ERP
- Complex accounting software

---

# AI Agent Role

You are the Lead Software Architect, Senior Python Engineer, Database Designer and Project Maintainer.

Your responsibility:

- Design
- Implement
- Test
- Document
- Maintain

The repository is the main product.

Chat messages are secondary.

---

# Autonomous Mode

Work autonomously whenever possible.

Do not ask unnecessary questions.

Do not stop for minor decisions.

When multiple solutions exist:

Choose the solution with:

1. Lowest complexity
2. Highest maintainability
3. Best readability
4. Long-term stability

Only ask for approval when a decision can create major architectural changes.

---

# Token Optimization

Optimize communication and token usage.

Rules:

- Do not explain obvious code.
- Do not print large code blocks in chat.
- Prefer modifying repository files.
- Keep responses short.
- Store explanations in documentation files.

The repository documentation is the source of truth.

---

# Technology Stack

Backend:

FastAPI

Database:

PostgreSQL

ORM:

SQLAlchemy 2

Migration:

Alembic

Frontend:

Jinja2
HTMX
Alpine.js
Bootstrap RTL

Language:

Python 3.12+

---

# Architecture Rules

Use:

- Clean Architecture
- Service Layer
- Repository Pattern
- Dependency Injection
- Modular Design

Avoid:

- Over engineering
- Deep unnecessary abstractions
- Large files
- Tight coupling

---

# Project Structure

Preferred:

app/

    core/
    models/
    schemas/
    routers/
    services/
    repositories/
    templates/
    static/
    plugins/


Each module must have a clear responsibility.

---

# Plugin Architecture

ClinicCore must support medical specialty plugins.

Core modules must remain generic.

Examples:

plugins/

    psychology

    dentistry

    physiotherapy

    nutrition

    speech_therapy


A specialty feature should be a plugin whenever possible.

---

# Persian First

The system must support:

- RTL
- Persian UI
- Jalali calendar
- Persian numbers
- Iranian holidays
- UTF-8
- Persian reports

from the beginning.

---

# Database Rules

Use:

- SQLAlchemy models
- Alembic migrations

Never modify database manually.

Every database change requires migration.

Use:

- Soft delete where needed
- Created_at
- Updated_at
- Audit fields

---

# Development Workflow

Every feature follows:

1. Analysis
2. Design
3. Implementation
4. Testing
5. Documentation
6. Commit


---

# Sprint Management

Development must be Sprint based.

Before each Sprint create:

HELP/SPRINT_X.md


Include:

- Goal
- Tasks
- Files affected
- Database changes
- Risks
- Test plan


After completion update:

HELP/ROADMAP.txt

HELP/CHANGELOG.txt

---

# Documentation Rules

Maintain:

HELP/

    INSTALL.txt

    RUN.txt

    ARCHITECTURE.txt

    DATABASE.txt

    ROADMAP.txt

    DECISIONS.txt

    CHANGELOG.txt

    TODO.txt


Documentation must always match the current project state.

---

# Git Rules

Use small meaningful commits.

Examples:

Good:

"Add patient model"

"Implement appointment service"

"Create Jalali calendar module"


Bad:

"Update files"

"Changes"

---

# Testing

Every important feature requires tests.

Priority:

1. Business logic
2. Database operations
3. API endpoints

---

# Security

Implement:

- Secure password hashing
- Role based permissions
- Input validation
- CSRF protection
- Audit logging

---

# Performance Goals

Initial target:

- 1000 patients
- 50 doctors
- 100 appointments/day

Optimize only when required.

---

# Financial Module

Keep financial features simple.

Required:

- Payments
- Expenses
- Cash box
- Doctor share
- Clinic share
- Patient balance


Do NOT create full accounting ERP.

---

# Appointment Module

Support:

- Booking
- Rescheduling
- Cancellation
- Waiting list
- No-show
- Completed visits
- Reminders

---

# Messaging System

Use provider architecture.

Possible providers:

- SMS
- Email
- Telegram
- WhatsApp
- Iranian messengers


Never hardcode one provider.

---

# Final Goal

A developer should be able to:

1. Clone repository
2. Read HELP files
3. Install dependencies
4. Run project


The repository must always be understandable without external explanation.
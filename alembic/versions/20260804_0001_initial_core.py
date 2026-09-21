"""initial core tables

Revision ID: 20260804_0001
Revises:
Create Date: 2026-08-04
"""
from alembic import op
import sqlalchemy as sa

revision = "20260804_0001"
down_revision = None
branch_labels = None
depends_on = None

appointment_status = sa.Enum("booked", "rescheduled", "cancelled", "waiting", "no_show", "completed", name="appointmentstatus")


def upgrade() -> None:
    #appointment_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("national_code", sa.String(length=10), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("national_code"),
    )
    op.create_index(op.f("ix_patients_id"), "patients", ["id"])
    op.create_index(op.f("ix_patients_is_deleted"), "patients", ["is_deleted"])
    op.create_index(op.f("ix_patients_national_code"), "patients", ["national_code"])
    op.create_index(op.f("ix_patients_phone"), "patients", ["phone"])
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=200), nullable=True),
        sa.Column("status", appointment_status, nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_appointments_id"), "appointments", ["id"])
    op.create_index(op.f("ix_appointments_is_deleted"), "appointments", ["is_deleted"])
    op.create_index(op.f("ix_appointments_patient_id"), "appointments", ["patient_id"])
    op.create_index(op.f("ix_appointments_starts_at"), "appointments", ["starts_at"])


def downgrade() -> None:
    op.drop_table("appointments")
    op.drop_table("patients")
    appointment_status.drop(op.get_bind(), checkfirst=True)

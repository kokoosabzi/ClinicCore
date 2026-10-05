"""enforce one active appointment per shared time slot

Revision ID: 20261002_0004
Revises: 20260804_0003
Create Date: 2026-10-02
"""

from alembic import op
import sqlalchemy as sa


revision = "20261002_0004"
down_revision = "20260804_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "uq_active_appointment_starts_at",
        "appointments",
        ["starts_at"],
        unique=True,
        postgresql_where=sa.text("NOT is_deleted"),
        sqlite_where=sa.text("is_deleted = 0"),
    )


def downgrade() -> None:
    op.drop_index("uq_active_appointment_starts_at", table_name="appointments")

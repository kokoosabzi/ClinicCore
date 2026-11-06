"""allow cancelled appointments to release their time slot

Revision ID: 20261107_0007
Revises: 20261106_0006
Create Date: 2026-11-07
"""

from alembic import op
import sqlalchemy as sa


revision = "20261107_0007"
down_revision = "20261106_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("uq_active_appointment_starts_at", table_name="appointments")
    op.create_index(
        "uq_active_appointment_starts_at",
        "appointments",
        ["starts_at"],
        unique=True,
        postgresql_where=sa.text("NOT is_deleted AND status != 'cancelled'"),
        sqlite_where=sa.text("is_deleted = 0 AND status != 'cancelled'"),
    )


def downgrade() -> None:
    op.drop_index("uq_active_appointment_starts_at", table_name="appointments")
    op.create_index(
        "uq_active_appointment_starts_at",
        "appointments",
        ["starts_at"],
        unique=True,
        postgresql_where=sa.text("NOT is_deleted"),
        sqlite_where=sa.text("is_deleted = 0"),
    )

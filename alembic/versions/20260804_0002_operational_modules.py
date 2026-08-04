"""operational modules

Revision ID: 20260804_0002
Revises: 20260804_0001
Create Date: 2026-08-04
"""
from alembic import op
import sqlalchemy as sa

revision = "20260804_0002"
down_revision = "20260804_0001"
branch_labels = None
depends_on = None

user_role = sa.Enum("admin", "doctor", "secretary", "accountant", name="userrole")
payment_status = sa.Enum("pending", "paid", "refunded", name="paymentstatus")
expense_category = sa.Enum("rent", "salary", "supplies", "utilities", "other", name="expensecategory")
message_provider = sa.Enum("sms", "email", "telegram", "whatsapp", "iranian_messenger", name="messageprovider")
message_status = sa.Enum("queued", "sent", "failed", name="messagestatus")


def upgrade() -> None:
    bind = op.get_bind()
    for enum in [user_role, payment_status, expense_category, message_provider, message_status]:
        enum.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"])
    op.create_index(op.f("ix_users_is_deleted"), "users", ["is_deleted"])
    op.create_index(op.f("ix_users_username"), "users", ["username"])

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("paid_at", sa.Date(), nullable=False),
        sa.Column("status", payment_status, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payments_id"), "payments", ["id"])
    op.create_index(op.f("ix_payments_is_deleted"), "payments", ["is_deleted"])
    op.create_index(op.f("ix_payments_patient_id"), "payments", ["patient_id"])

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("spent_at", sa.Date(), nullable=False),
        sa.Column("category", expense_category, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_expenses_id"), "expenses", ["id"])
    op.create_index(op.f("ix_expenses_is_deleted"), "expenses", ["is_deleted"])

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipient", sa.String(length=120), nullable=False),
        sa.Column("provider", message_provider, nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", message_status, nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_id"), "messages", ["id"])
    op.create_index(op.f("ix_messages_recipient"), "messages", ["recipient"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor", sa.String(length=120), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_action"), "audit_logs", ["action"])
    op.create_index(op.f("ix_audit_logs_entity"), "audit_logs", ["entity"])
    op.create_index(op.f("ix_audit_logs_entity_id"), "audit_logs", ["entity_id"])


def downgrade() -> None:
    for table in ["audit_logs", "messages", "expenses", "payments", "users"]:
        op.drop_table(table)
    bind = op.get_bind()
    for enum in [message_status, message_provider, expense_category, payment_status, user_role]:
        enum.drop(bind, checkfirst=True)

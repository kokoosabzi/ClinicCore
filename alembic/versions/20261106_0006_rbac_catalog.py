"""add role and permission catalog

Revision ID: 20261106_0006
Revises: 20261005_0005
Create Date: 2026-11-06
"""

from alembic import op
import sqlalchemy as sa


revision = "20261106_0006"
down_revision = "20261005_0005"
branch_labels = None
depends_on = None


PERMISSIONS = [
    ("users.view", "مشاهده کاربران", "users"),
    ("users.create", "ایجاد کاربر", "users"),
    ("users.update", "ویرایش کاربر", "users"),
    ("users.deactivate", "فعال/غیرفعال‌سازی کاربر", "users"),
    ("users.reset_password", "بازنشانی رمز عبور", "users"),
    ("users.assign_role", "تخصیص نقش", "users"),
    ("roles.manage", "مدیریت مجوز نقش‌ها", "roles"),
    ("patients.view", "مشاهده بیماران", "patients"),
    ("patients.create", "ثبت بیمار", "patients"),
    ("patients.update", "ویرایش بیمار", "patients"),
    ("patients.archive", "بایگانی بیمار", "patients"),
    ("appointments.view", "مشاهده نوبت‌ها", "appointments"),
    ("appointments.create", "ثبت نوبت", "appointments"),
    ("appointments.update", "ویرایش نوبت", "appointments"),
    ("appointments.cancel", "لغو نوبت", "appointments"),
    ("financial.view", "مشاهده امور مالی", "financial"),
    ("financial.create", "ثبت امور مالی", "financial"),
    ("financial.update", "ویرایش امور مالی", "financial"),
    ("financial.void", "ابطال سند مالی", "financial"),
    ("messaging.view", "مشاهده پیام‌ها", "messaging"),
    ("messaging.create", "ایجاد پیام", "messaging"),
    ("reports.view", "مشاهده گزارش‌ها", "reports"),
    ("reports.financial", "گزارش‌های مالی", "reports"),
    ("settings.view", "مشاهده تنظیمات", "settings"),
    ("settings.update", "تغییر تنظیمات", "settings"),
    ("audit.view", "مشاهده رویدادهای سامانه", "audit"),
]

ALL = {item[0] for item in PERMISSIONS}
MANAGER = ALL - {"users.assign_role", "roles.manage", "settings.view", "settings.update"}
DOCTOR_SECRETARY = {
    "patients.view", "patients.create", "patients.update",
    "appointments.view", "appointments.create", "appointments.update", "appointments.cancel",
    "messaging.view", "messaging.create",
}
ACCOUNTANT = {
    "financial.view", "financial.create", "financial.update", "reports.financial",
}


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=40), nullable=False, unique=True),
        sa.Column("label", sa.String(length=80), nullable=False),
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_roles_key", "roles", ["key"], unique=True)

    op.create_table(
        "permissions",
        sa.Column("code", sa.String(length=80), primary_key=True),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("permission_code", sa.String(length=80), sa.ForeignKey("permissions.code", ondelete="CASCADE"), primary_key=True),
    )

    connection = op.get_bind()
    roles = sa.table(
        "roles",
        sa.column("id", sa.Integer()),
        sa.column("key", sa.String()),
        sa.column("label", sa.String()),
        sa.column("is_system", sa.Boolean()),
        sa.column("is_active", sa.Boolean()),
    )
    permissions = sa.table(
        "permissions",
        sa.column("code", sa.String()),
        sa.column("label", sa.String()),
        sa.column("category", sa.String()),
    )
    grants = sa.table(
        "role_permissions",
        sa.column("role_id", sa.Integer()),
        sa.column("permission_code", sa.String()),
    )

    role_rows = [
        {"id": 1, "key": "admin", "label": "مدیر سیستم", "is_system": True, "is_active": True},
        {"id": 2, "key": "clinic_manager", "label": "مدیر کلینیک", "is_system": True, "is_active": True},
        {"id": 3, "key": "doctor", "label": "پزشک", "is_system": True, "is_active": True},
        {"id": 4, "key": "secretary", "label": "پذیرش", "is_system": True, "is_active": True},
        {"id": 5, "key": "accountant", "label": "حسابدار", "is_system": True, "is_active": True},
    ]
    connection.execute(roles.insert(), role_rows)
    connection.execute(
        permissions.insert(),
        [{"code": code, "label": label, "category": category} for code, label, category in PERMISSIONS],
    )

    role_grants = []
    role_permissions = {
        "admin": ALL,
        "clinic_manager": MANAGER,
        "doctor": DOCTOR_SECRETARY,
        "secretary": DOCTOR_SECRETARY,
        "accountant": ACCOUNTANT,
    }
    for role_id, role in enumerate(role_rows, start=1):
        for permission in sorted(role_permissions[role["key"]]):
            role_grants.append({"role_id": role_id, "permission_code": permission})
    connection.execute(grants.insert(), role_grants)


def downgrade() -> None:
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_index("ix_roles_key", table_name="roles")
    op.drop_table("roles")

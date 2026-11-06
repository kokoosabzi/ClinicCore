from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.role import Permission, Role, RolePermission


class RoleManagementError(ValueError):
    pass


class RoleService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_roles(self) -> list[dict]:
        roles = list(self.db.scalars(select(Role).where(Role.is_active.is_(True)).order_by(Role.id)))
        permissions = list(self.db.scalars(select(Permission).order_by(Permission.category, Permission.code)))
        result = []
        for role in roles:
            granted = set(
                self.db.scalars(
                    select(RolePermission.permission_code).where(RolePermission.role_id == role.id)
                )
            )
            result.append(
                {
                    "role": role,
                    "permissions": permissions,
                    "granted": granted,
                }
            )
        return result

    def update_permissions(self, role_key: str, permission_codes: set[str]) -> None:
        role = self.db.scalar(select(Role).where(Role.key == role_key, Role.is_active.is_(True)))
        if role is None:
            raise RoleManagementError("نقش موردنظر پیدا نشد.")
        if role.key == "admin":
            raise RoleManagementError("مجوزهای مدیر سیستم ثابت و غیرقابل تغییر هستند.")

        known = set(self.db.scalars(select(Permission.code)))
        unknown = permission_codes - known
        if unknown:
            raise RoleManagementError("یک یا چند مجوز انتخاب‌شده معتبر نیست.")
        if "roles.manage" in permission_codes:
            raise RoleManagementError("مدیریت مجوز نقش‌ها فقط در اختیار مدیر سیستم است.")

        try:
            self.db.execute(delete(RolePermission).where(RolePermission.role_id == role.id))
            self.db.add_all(
                RolePermission(role_id=role.id, permission_code=code)
                for code in sorted(permission_codes)
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

from secrets import token_urlsafe

from app.core.security import hash_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserManagementError(ValueError):
    pass


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list_users(self) -> list[User]:
        return self.repository.list()

    def create_user(self, data: UserCreate) -> User:
        username = data.username.strip()
        if self.repository.username_exists(username):
            raise UserManagementError("این نام کاربری قبلاً ثبت شده است.")
        if not self.repository.role_exists(data.role):
            raise UserManagementError("نقش انتخاب‌شده معتبر یا فعال نیست.")
        entity = User(
            full_name=data.full_name.strip(),
            username=username,
            password_hash=hash_password(data.password),
            role=data.role,
            must_change_password=True,
        )
        return self.repository.create(entity)

    def update_user(
        self,
        user_id: int,
        data: UserUpdate,
        *,
        actor_role: UserRole,
        can_assign_role: bool,
    ) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserManagementError("کاربر موردنظر پیدا نشد.")
        if actor_role != UserRole.admin and user.role == UserRole.admin:
            raise UserManagementError("مدیر کلینیک اجازه تغییر حساب مدیر سیستم را ندارد.")
        if data.role != user.role and not can_assign_role:
            raise UserManagementError("تغییر نقش برای حساب شما مجاز نیست.")
        if not self.repository.role_exists(data.role):
            raise UserManagementError("نقش انتخاب‌شده معتبر یا فعال نیست.")
        if user.role == UserRole.admin and data.role != UserRole.admin:
            if self.repository.active_admin_count() <= 1:
                raise UserManagementError("تغییر نقش آخرین مدیر سیستم مجاز نیست.")
        if data.role == UserRole.admin and actor_role != UserRole.admin:
            raise UserManagementError("فقط مدیر سیستم می‌تواند نقش مدیر سیستم را واگذار کند.")
        user.full_name = data.full_name.strip()
        user.role = data.role
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user

    def set_active(
        self,
        user_id: int,
        *,
        active: bool,
        actor_id: int,
        actor_role: UserRole,
    ) -> User:
        user = self.repository.get_by_id(user_id, include_deleted=active)
        if user is None:
            raise UserManagementError("کاربر موردنظر پیدا نشد.")
        if user.id == actor_id and not active:
            raise UserManagementError("غیرفعال‌سازی حساب کاربری خودتان مجاز نیست.")
        if actor_role != UserRole.admin and user.role == UserRole.admin:
            raise UserManagementError("مدیر کلینیک اجازه تغییر وضعیت مدیر سیستم را ندارد.")
        if user.role == UserRole.admin and not active and self.repository.active_admin_count() <= 1:
            raise UserManagementError("غیرفعال‌سازی آخرین مدیر سیستم مجاز نیست.")
        user.is_deleted = not active
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user

    def reset_password(
        self,
        user_id: int,
        *,
        actor_role: UserRole,
    ) -> tuple[User, str]:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserManagementError("کاربر موردنظر پیدا نشد.")
        if actor_role != UserRole.admin and user.role == UserRole.admin:
            raise UserManagementError("مدیر کلینیک اجازه بازنشانی رمز مدیر سیستم را ندارد.")
        temporary_password = token_urlsafe(12)
        user.password_hash = hash_password(temporary_password)
        user.must_change_password = True
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user, temporary_password

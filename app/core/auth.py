from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.role import Role, RolePermission
from app.models.user import User, UserRole


def current_user(request: Request) -> dict[str, str] | None:
    username = request.session.get("username")
    role = request.session.get("role")
    if not username or not role:
        return None
    return {"username": username, "role": role}


def _authenticated_user(request: Request, db: Session) -> User:
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    user = db.scalar(
        select(User).where(User.username == username, User.is_deleted.is_(False))
    )
    if user is None:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    allowed_during_password_change = {"/change-password", "/logout"}
    if user.must_change_password and request.url.path not in allowed_during_password_change:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password change required before accessing this resource",
        )
    return user


def _principal(user: User) -> dict[str, str | int]:
    return {"id": user.id, "username": user.username, "role": user.role.value}


def require_user(request: Request, db: Session = Depends(get_db)) -> dict[str, str | int]:
    return _principal(_authenticated_user(request, db))


def require_admin(request: Request, db: Session = Depends(get_db)) -> dict[str, str | int]:
    user = _authenticated_user(request, db)
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return _principal(user)


def has_permission(db: Session, role: UserRole | str, permission_code: str) -> bool:
    role_key = role.value if isinstance(role, UserRole) else str(role)
    statement = (
        select(RolePermission.role_id)
        .join(Role, Role.id == RolePermission.role_id)
        .where(
            Role.key == role_key,
            Role.is_active.is_(True),
            RolePermission.permission_code == permission_code,
        )
        .limit(1)
    )
    return db.scalar(statement) is not None


def require_permission(permission_code: str) -> Callable:
    def dependency(
        request: Request,
        db: Session = Depends(get_db),
    ) -> dict[str, str | int]:
        user = _authenticated_user(request, db)
        if not has_permission(db, user.role, permission_code):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return _principal(user)

    return dependency

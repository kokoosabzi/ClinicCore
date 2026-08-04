from fastapi import HTTPException, Request, status

from app.models.user import UserRole


def current_user(request: Request) -> dict[str, str] | None:
    username = request.session.get("username")
    role = request.session.get("role")
    if not username or not role:
        return None
    return {"username": username, "role": role}


def require_user(request: Request) -> dict[str, str]:
    user = current_user(request)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user


def require_admin(request: Request) -> dict[str, str]:
    user = require_user(request)
    if user["role"] != UserRole.admin.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

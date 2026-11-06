from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.auth import current_user, has_permission, require_permission
from app.core.csrf import get_csrf_token, verify_csrf
from app.core.database import get_db
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserResetPasswordResult, UserUpdate
from app.services.role_service import RoleManagementError, RoleService
from app.services.user_service import UserManagementError, UserService

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="app/templates")


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


async def read_form(request: Request) -> dict[str, str]:
    body = (await request.body()).decode("utf-8")
    return {key: values[-1] for key, values in parse_qs(body, keep_blank_values=True).items()}


def render_manage(
    request: Request,
    service: UserService,
    *,
    actor: dict,
    error: str | None = None,
    notice: str | None = None,
    temporary_password: str | None = None,
    status_code: int = 200,
):
    db = service.repository.db
    role_labels = {
        "admin": "مدیر سیستم",
        "clinic_manager": "مدیر کلینیک",
        "doctor": "پزشک",
        "secretary": "پذیرش",
        "accountant": "حسابدار",
    }
    users = service.list_users(include_inactive=True)
    return templates.TemplateResponse(
        request=request,
        name="users/manage.html",
        context={
            "request": request,
            "title": "مدیریت کاربران",
            "user": getattr(request.state, "current_user", None) or current_user(request),
            "permissions": getattr(request.state, "permissions", set()),
            "csrf_token": get_csrf_token(request),
            "users": users,
            "roles": list(UserRole),
            "role_labels": role_labels,
            "error": error,
            "notice": notice,
            "temporary_password": temporary_password,
            "can_create": has_permission(db, actor["role"], "users.create"),
            "can_update": has_permission(db, actor["role"], "users.update"),
            "can_assign_role": has_permission(db, actor["role"], "users.assign_role"),
            "can_deactivate": has_permission(db, actor["role"], "users.deactivate"),
            "can_reset_password": has_permission(db, actor["role"], "users.reset_password"),
            "actor_id": actor["id"],
        },
        status_code=status_code,
    )



@router.get("/roles", response_class=HTMLResponse)
def manage_roles(
    request: Request,
    user=Depends(require_permission("roles.manage")),
    db: Session = Depends(get_db),
):
    service = RoleService(db)
    return templates.TemplateResponse(
        request=request,
        name="users/roles.html",
        context={
            "request": request,
            "title": "مدیریت نقش‌ها و مجوزها",
            "user": getattr(request.state, "current_user", None) or current_user(request),
            "permissions": getattr(request.state, "permissions", set()),
            "csrf_token": get_csrf_token(request),
            "roles_data": service.list_roles(),
            "error": None,
            "notice": None,
        },
    )


@router.post("/roles/{role_key}", response_class=HTMLResponse)
async def update_role_permissions(
    role_key: str,
    request: Request,
    user=Depends(require_permission("roles.manage")),
    db: Session = Depends(get_db),
):
    form = await request.form()
    verify_csrf(request, form.get("csrf_token"))
    permission_codes = set(form.getlist("permissions"))
    service = RoleService(db)
    try:
        service.update_permissions(role_key, permission_codes)
    except RoleManagementError as error:
        return templates.TemplateResponse(
            request=request,
            name="users/roles.html",
            context={
                "request": request,
                "title": "مدیریت نقش‌ها و مجوزها",
                "user": current_user(request),
                "csrf_token": get_csrf_token(request),
                "roles_data": service.list_roles(),
                "error": str(error),
                "notice": None,
            },
            status_code=409,
        )
    return RedirectResponse(url="/users/roles?saved=1", status_code=303)

@router.get("/", response_model=list[UserRead])
def list_users(
    user=Depends(require_permission("users.view")),
    service: UserService = Depends(get_service),
):
    return service.list_users()


@router.get("/manage", response_class=HTMLResponse)
def manage_users(
    request: Request,
    user=Depends(require_permission("users.view")),
    service: UserService = Depends(get_service),
):
    return render_manage(request, service, actor=user)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    user=Depends(require_permission("users.create")),
    service: UserService = Depends(get_service),
):
    actor_role = UserRole(user["role"])
    if payload.role != UserRole.secretary and not has_permission(
        service.repository.db, actor_role, "users.assign_role"
    ):
        raise HTTPException(status_code=403, detail="Role assignment is not permitted")
    try:
        return service.create_user(payload)
    except UserManagementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    user=Depends(require_permission("users.update")),
    service: UserService = Depends(get_service),
):
    actor_role = UserRole(user["role"])
    can_assign_role = has_permission(service.repository.db, actor_role, "users.assign_role")
    try:
        return service.update_user(
            user_id, payload, actor_role=actor_role, can_assign_role=can_assign_role
        )
    except UserManagementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/{user_id}/deactivate", response_model=UserRead)
def deactivate_user(
    user_id: int,
    user=Depends(require_permission("users.deactivate")),
    service: UserService = Depends(get_service),
):
    try:
        return service.set_active(
            user_id, active=False, actor_id=int(user["id"]), actor_role=UserRole(user["role"])
        )
    except UserManagementError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/{user_id}/reactivate", response_model=UserRead)
def reactivate_user(
    user_id: int,
    user=Depends(require_permission("users.deactivate")),
    service: UserService = Depends(get_service),
):
    try:
        return service.set_active(
            user_id, active=True, actor_id=int(user["id"]), actor_role=UserRole(user["role"])
        )
    except UserManagementError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{user_id}/reset-password", response_model=UserResetPasswordResult)
def reset_password(
    user_id: int,
    user=Depends(require_permission("users.reset_password")),
    service: UserService = Depends(get_service),
):
    try:
        target, temporary_password = service.reset_password(
            user_id, actor_role=UserRole(user["role"])
        )
    except UserManagementError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return UserResetPasswordResult(user_id=target.id, temporary_password=temporary_password)


@router.post("/ui/create", response_class=HTMLResponse)
async def create_user_from_form(
    request: Request,
    user=Depends(require_permission("users.create")),
    service: UserService = Depends(get_service),
):
    data = await read_form(request)
    verify_csrf(request, data.get("csrf_token"))
    try:
        payload = UserCreate(
            full_name=data.get("full_name", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=UserRole(data.get("role", "secretary")),
        )
    except ValueError as error:
        return render_manage(request, service, actor=user, error="اطلاعات کاربر معتبر نیست.", status_code=422)
    actor_role = UserRole(user["role"])
    if payload.role != UserRole.secretary and not has_permission(
        service.repository.db, actor_role, "users.assign_role"
    ):
        raise HTTPException(status_code=403, detail="Role assignment is not permitted")
    try:
        service.create_user(payload)
    except UserManagementError as error:
        return render_manage(request, service, actor=user, error=str(error), status_code=409)
    return RedirectResponse(url="/users/manage?created=1", status_code=303)


@router.post("/ui/{user_id}/update", response_class=HTMLResponse)
async def update_user_from_form(
    user_id: int,
    request: Request,
    user=Depends(require_permission("users.update")),
    service: UserService = Depends(get_service),
):
    data = await read_form(request)
    verify_csrf(request, data.get("csrf_token"))
    try:
        payload = UserUpdate(
            full_name=data.get("full_name", ""),
            role=UserRole(data.get("role", "")),
        )
        service.update_user(
            user_id,
            payload,
            actor_role=UserRole(user["role"]),
            can_assign_role=has_permission(service.repository.db, user["role"], "users.assign_role"),
        )
    except (ValueError, UserManagementError) as error:
        message = str(error) if isinstance(error, UserManagementError) else "اطلاعات کاربر معتبر نیست."
        return render_manage(request, service, actor=user, error=message, status_code=409)
    return RedirectResponse(url="/users/manage?updated=1", status_code=303)


@router.post("/ui/{user_id}/deactivate", response_class=HTMLResponse)
async def deactivate_user_from_form(
    user_id: int,
    request: Request,
    user=Depends(require_permission("users.deactivate")),
    service: UserService = Depends(get_service),
):
    data = await read_form(request)
    verify_csrf(request, data.get("csrf_token"))
    try:
        service.set_active(
            user_id, active=False, actor_id=int(user["id"]), actor_role=UserRole(user["role"])
        )
    except UserManagementError as error:
        return render_manage(request, service, actor=user, error=str(error), status_code=409)
    return RedirectResponse(url="/users/manage?deactivated=1", status_code=303)


@router.post("/ui/{user_id}/reactivate", response_class=HTMLResponse)
async def reactivate_user_from_form(
    user_id: int,
    request: Request,
    user=Depends(require_permission("users.deactivate")),
    service: UserService = Depends(get_service),
):
    data = await read_form(request)
    verify_csrf(request, data.get("csrf_token"))
    try:
        service.set_active(
            user_id, active=True, actor_id=int(user["id"]), actor_role=UserRole(user["role"])
        )
    except UserManagementError as error:
        return render_manage(request, service, actor=user, error=str(error), status_code=409)
    return RedirectResponse(url="/users/manage?reactivated=1", status_code=303)


@router.post("/ui/{user_id}/reset-password", response_class=HTMLResponse)
async def reset_password_from_form(
    user_id: int,
    request: Request,
    user=Depends(require_permission("users.reset_password")),
    service: UserService = Depends(get_service),
):
    data = await read_form(request)
    verify_csrf(request, data.get("csrf_token"))
    try:
        target, temporary_password = service.reset_password(
            user_id, actor_role=UserRole(user["role"])
        )
    except UserManagementError as error:
        return render_manage(request, service, actor=user, error=str(error), status_code=404)
    return render_manage(
        request,
        service,
        actor=user,
        notice=f"رمز موقت برای کاربر {target.username} ایجاد شد. این رمز فقط در همین صفحه نمایش داده می‌شود.",
        temporary_password=temporary_password,
    )

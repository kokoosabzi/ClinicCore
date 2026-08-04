from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.csrf import get_csrf_token, verify_csrf
from app.core.database import get_db
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["auth"])


async def form_data(request: Request) -> dict[str, str]:
    body = (await request.body()).decode("utf-8")
    return {key: values[-1] for key, values in parse_qs(body, keep_blank_values=True).items()}


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "title": "ورود"})


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await form_data(request)
    user = AuthService(UserRepository(db)).authenticate(data.get("username", ""), data.get("password", ""))
    if user is None:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "title": "ورود", "error": "نام کاربری یا رمز عبور نادرست است."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    request.session["username"] = user.username
    request.session["role"] = user.role.value
    if user.must_change_password:
        return RedirectResponse(url="/change-password", status_code=303)
    return RedirectResponse(url="/dashboard", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@router.get("/change-password", response_class=HTMLResponse)
def change_password_form(request: Request):
    return templates.TemplateResponse("auth/change_password.html", {"request": request, "title": "تغییر رمز", "csrf_token": get_csrf_token(request)})


@router.post("/change-password")
async def change_password(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    data = await form_data(request)
    verify_csrf(request, data.get("csrf_token"))
    password = data.get("password", "")
    confirm = data.get("confirm", "")
    if password != confirm or len(password) < 8:
        return templates.TemplateResponse(
            "auth/change_password.html",
            {"request": request, "title": "تغییر رمز", "csrf_token": get_csrf_token(request), "error": "رمز باید حداقل ۸ کاراکتر باشد و با تکرار آن یکسان باشد."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user = UserRepository(db).get_by_username(username)
    if user is None:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)
    user.password_hash = hash_password(password)
    user.must_change_password = False
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

from secrets import token_urlsafe

from fastapi import HTTPException, Request, status

CSRF_SESSION_KEY = "csrf_token"


def get_csrf_token(request: Request) -> str:
    token = request.session.get(CSRF_SESSION_KEY)
    if not token:
        token = token_urlsafe(32)
        request.session[CSRF_SESSION_KEY] = token
    return token


def verify_csrf(request: Request, token: str | None) -> None:
    expected = request.session.get(CSRF_SESSION_KEY)
    if not expected or not token or token != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")

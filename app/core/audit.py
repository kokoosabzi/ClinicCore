from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal
from app.services.audit_service import AuditService


async def audit_request_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)
    if request.url.path.startswith(("/static", "/health")):
        return response
    actor = request.session.get("username") if "session" in request.scope else None
    details = f"{request.method} {request.url.path} -> {response.status_code}"
    db = SessionLocal()
    try:
        AuditService(db).log(action="http_request", entity="system", actor=actor, details=details)
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()
    return response

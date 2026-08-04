from sqlalchemy.orm import Session

from app.models.audit import AuditLog


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def log(self, action: str, entity: str, actor: str | None = None, entity_id: str | None = None, details: str | None = None) -> None:
        self.db.add(AuditLog(actor=actor, action=action, entity=entity, entity_id=entity_id, details=details))
        self.db.commit()

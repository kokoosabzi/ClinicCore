from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class Repository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[ModelT]:
        statement = select(self.model).order_by(self.model.id)  # type: ignore[attr-defined]
        if hasattr(self.model, "is_deleted"):
            statement = statement.where(self.model.is_deleted.is_(False))  # type: ignore[attr-defined]
        return list(self.db.scalars(statement))

    def create(self, entity: ModelT) -> ModelT:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

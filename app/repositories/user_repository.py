from sqlalchemy import select

from app.models.role import Role
from app.models.user import User, UserRole
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    model = User

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username, User.is_deleted.is_(False)))

    def get_by_id(self, user_id: int, *, include_deleted: bool = False) -> User | None:
        statement = select(User).where(User.id == user_id)
        if not include_deleted:
            statement = statement.where(User.is_deleted.is_(False))
        return self.db.scalar(statement)

    def username_exists(self, username: str, *, excluding_id: int | None = None) -> bool:
        statement = select(User.id).where(User.username == username)
        if excluding_id is not None:
            statement = statement.where(User.id != excluding_id)
        return self.db.scalar(statement.limit(1)) is not None

    def role_exists(self, role: UserRole) -> bool:
        return self.db.scalar(select(Role.id).where(Role.key == role.value, Role.is_active.is_(True))) is not None

    def active_admin_count(self) -> int:
        return len(
            list(
                self.db.scalars(
                    select(User.id).where(
                        User.role == UserRole.admin,
                        User.is_deleted.is_(False),
                    )
                )
            )
        )

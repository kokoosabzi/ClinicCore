from sqlalchemy import select

from app.models.user import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    model = User

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username, User.is_deleted.is_(False)))

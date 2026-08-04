from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.users.get_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            return None
        return user

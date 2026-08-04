from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list_users(self) -> list[User]:
        return self.repository.list()

    def create_user(self, data: UserCreate) -> User:
        payload = data.model_dump(exclude={"password"})
        payload["password_hash"] = hash_password(data.password)
        return self.repository.create(User(**payload))

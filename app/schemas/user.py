from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.user import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    username: str = Field(min_length=3, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.secretary

    @field_validator("full_name")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("نام کامل الزامی است.")
        return normalized


class UserUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    role: UserRole

    @field_validator("full_name")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("نام کامل الزامی است.")
        return normalized


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: UserRole
    must_change_password: bool
    is_deleted: bool
    model_config = ConfigDict(from_attributes=True)


class UserResetPasswordResult(BaseModel):
    user_id: int
    temporary_password: str
    must_change_password: bool = True

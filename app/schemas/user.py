from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8)
    role: UserRole = UserRole.secretary


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: UserRole
    must_change_password: bool
    model_config = ConfigDict(from_attributes=True)

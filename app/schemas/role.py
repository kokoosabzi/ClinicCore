from pydantic import BaseModel, Field


class RolePermissionsUpdate(BaseModel):
    permissions: set[str] = Field(default_factory=set)

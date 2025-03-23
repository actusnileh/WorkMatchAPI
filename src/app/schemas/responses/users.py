from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    UUID4,
)

from app.models import User


class UserResponse(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "john.doe@example.com"})
    username: str = Field(..., json_schema_extra={"example": "john.doe"})
    full_name: str = Field(..., json_schema_extra={"example": "Петров Николай Петрович"})
    role: str = Field(..., json_schema_extra={"example": "user"})
    uuid: UUID4 = Field(..., json_schema_extra={"example": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"})

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, user: User) -> "UserResponse":
        return cls(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role.name if user.role else "unknown",
            uuid=user.uuid,
        )


class RegisterUserResponse(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "john.doe@example.com"})
    username: str = Field(..., json_schema_extra={"example": "john.doe"})
    full_name: str = Field(..., json_schema_extra={"example": "Петров Николай Петрович"})
    uuid: UUID4 = Field(..., json_schema_extra={"example": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"})

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, user: User) -> "UserResponse":
        return cls(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            uuid=user.uuid,
        )

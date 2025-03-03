from pydantic import (
    BaseModel,
    Field,
    UUID4,
)

from app.models import User


class UserResponse(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")
    full_name: str = Field(..., example="Петров Петр Петрович")
    role: str = Field(..., example="user")
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")

    class Config:
        from_attributes = True

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
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")
    full_name: str = Field(..., example="Петров Петр Петрович")
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, user: User) -> "UserResponse":
        return cls(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            uuid=user.uuid,
        )

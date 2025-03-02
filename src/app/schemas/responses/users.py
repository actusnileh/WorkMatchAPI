from typing import Type

from pydantic import (
    BaseModel,
    Field,
    UUID4,
)


class UserResponse(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")
    full_name: str = Field(..., example="Петров Петр Петрович")
    role: str = Field(..., example="user")
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm_instance(orm_instance: Type) -> "UserResponse":
        return UserResponse(
            email=orm_instance.email,
            username=orm_instance.username,
            full_name=orm_instance.full_name,
            role=orm_instance.role.name if orm_instance.role else "unknown",
            uuid=orm_instance.uuid,
        )

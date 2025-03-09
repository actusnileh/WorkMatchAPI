# pylint: disable=all

import re
from enum import Enum

from pydantic import (
    BaseModel,
    constr,
    EmailStr,
    field_validator,
)


class RoleName(str, Enum):
    USER = "user"
    HR = "hr"


class EmploymentTypeName(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)
    username: constr(min_length=3, max_length=64)
    full_name: constr(min_length=3, max_length=64)
    role: RoleName

    @field_validator("password")
    def password_must_contain_numbers(cls, v):
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

    @field_validator("username")
    def username_must_not_contain_special_characters(cls, v):
        if re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Username must not contain special characters")
        return v


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class EditUserRequest(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    username: str | None = None


class EditPasswordRequest(BaseModel):
    old_password: str
    new_password: constr(min_length=8, max_length=64)

    @field_validator("new_password")
    def password_must_contain_numbers(cls, v):
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

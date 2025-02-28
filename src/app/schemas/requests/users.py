# pylint: disable=all

import re

from pydantic import (
    BaseModel,
    constr,
    EmailStr,
    field_validator,
)


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)
    username: constr(min_length=3, max_length=64)

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

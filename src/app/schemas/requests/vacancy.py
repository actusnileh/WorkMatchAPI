from pydantic import (
    BaseModel,
    constr,
    PositiveFloat,
)


class CreateVacancyRequest(BaseModel):
    title: constr(min_length=4, max_length=64)
    description: constr(min_length=8, max_length=256)
    requirements: constr(min_length=8, max_length=256)
    conditions: constr(min_length=8, max_length=256)
    salary: PositiveFloat
    employment_type_str: str


class EditVacancyRequest(BaseModel):
    description: constr(min_length=8, max_length=256) | None = None
    requirements: constr(min_length=8, max_length=256) | None = None
    conditions: constr(min_length=8, max_length=256) | None = None
    salary: PositiveFloat | None = None
    employment_type_str: str | None = None

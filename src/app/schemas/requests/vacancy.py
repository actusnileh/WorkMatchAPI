from pydantic import (
    BaseModel,
    PositiveFloat,
)


class CreateVacancyRequest(BaseModel):
    title: str
    description: str
    requirements: str
    conditions: str
    salary: PositiveFloat
    employment_type_str: str


class EditVacancyRequest(BaseModel):
    description: str | None = None
    requirements: str | None = None
    conditions: str | None = None
    salary: PositiveFloat | None = None
    employment_type_str: str | None = None

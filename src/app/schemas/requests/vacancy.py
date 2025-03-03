from pydantic import (
    BaseModel,
    constr,
    PositiveFloat,
)


class CreateVacancyRequest(BaseModel):
    title: constr(min_length=8, max_length=64)
    description: constr(min_length=8, max_length=64)
    requirements: constr(min_length=8, max_length=64)
    conditions: constr(min_length=8, max_length=64)
    salary: PositiveFloat
    employment_type_str: str

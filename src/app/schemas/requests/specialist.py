from datetime import (
    date,
    datetime,
)
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


class SpecialistRequest(BaseModel):
    position: str
    about_me: str
    employment_type_str: str


class EditSpecialistRequest(BaseModel):
    position: str | None = None
    about_me: str | None = None
    employment_type_str: str | None = None


class AddSkillSpecialistRequest(BaseModel):
    skill: str


class AddExperienceSpecialistRequest(BaseModel):
    company_name: str
    position: str
    start_date: date
    end_date: Optional[date] = Field(None, description="Leave empty if currently working")

    @model_validator(mode="before")
    def check_dates(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        if isinstance(end_date, str) and end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date and start_date > date.today():
            raise ValueError("start_date cannot be in the future")

        if end_date and end_date > date.today():
            raise ValueError("end_date cannot be in the future")

        if end_date and start_date and end_date < start_date:
            raise ValueError("end_date must be after start_date")

        return values

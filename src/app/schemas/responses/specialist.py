from datetime import date
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    UUID4,
)

from app.models import Specialist


class SpecialistResponse(BaseModel):
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    full_name: str = Field(..., example="Петров Пётр Петрович")
    position: str = Field(..., example="Junior")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, specialist: Specialist):
        return cls(
            uuid=specialist.uuid,
            full_name=specialist.full_name,
            position=specialist.position,
        )


class ExperienceResponse(BaseModel):
    company_name: str
    position: str
    start_date: date
    end_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class SpecialistResponseWithAdditional(BaseModel):
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    full_name: str = Field(..., example="Петров Пётр Петрович")
    position: str = Field(..., example="Junior")
    skills: list[str] = Field(..., example=["SQL", "Backend", "Frontend"])
    experiences: list[ExperienceResponse] = Field(..., description="List of work experiences")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, specialist: Specialist):
        return cls(
            uuid=specialist.uuid,
            full_name=specialist.full_name,
            position=specialist.position,
            skills=[skill.skill_name for skill in specialist.skills],
            experiences=[
                ExperienceResponse(
                    company_name=exp.company_name,
                    position=exp.position,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                )
                for exp in specialist.experiences
            ],
        )

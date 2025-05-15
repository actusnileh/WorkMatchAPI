from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    UUID4,
)

from app.models import Specialist, EmploymentType


class SpecialistResponse(BaseModel):
    uuid: UUID4 = Field(..., json_schema_extra={"example": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"})
    full_name: str = Field(..., json_schema_extra={"example": "Петров Пётр Петрович"})
    position: str = Field(..., json_schema_extra={"example": "Junior"})
    about_me: str = Field(..., json_schema_extra={"example": "Изучал джанго, фастапи ..."})
    employment_type: str = Field(..., json_schema_extra={"example": "full-time"})

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, specialist: Specialist, employment_type: EmploymentType = None):
        return cls(
            uuid=specialist.uuid,
            full_name=specialist.full_name,
            about_me=specialist.about_me,
            position=specialist.position,
            employment_type=employment_type.name if employment_type is not None else specialist.employment_type.name,
        )


class ExperienceResponse(BaseModel):
    uuid: UUID
    company_name: str
    position: str
    start_date: date
    end_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class SpecialistResponseWithAdditional(BaseModel):
    uuid: UUID4 = Field(..., json_schema_extra={"example": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"})
    full_name: str = Field(..., json_schema_extra={"example": "Петров Пётр Петрович"})
    position: str = Field(..., json_schema_extra={"example": "Junior"})
    skills: list[str] = Field(..., json_schema_extra={"example": ["SQL", "Backend", "Frontend"]})
    experiences: list[ExperienceResponse] = Field(..., json_schema_extra={"example": "List of work experiences"})
    about_me: str = Field(..., json_schema_extra={"example": "Изучал джанго, фастапи ..."})

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
                    uuid=exp.uuid,
                    company_name=exp.company_name,
                    position=exp.position,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                )
                for exp in specialist.experiences
            ],
            about_me=specialist.about_me,
        )


class ListSpecialistResponseWithAdditional(BaseModel):
    Specialists: list[SpecialistResponseWithAdditional]

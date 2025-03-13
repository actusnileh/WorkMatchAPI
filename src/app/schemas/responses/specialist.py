from pydantic import (
    BaseModel,
    Field,
    UUID4,
)

from app.models import Specialist


class SpecialistResponse(BaseModel):
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    full_name: str = Field(..., example="Петров Пётр Петрович")
    position: str = Field(..., example="Junior")

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, specialist: Specialist):
        return cls(
            uuid=specialist.uuid,
            full_name=specialist.full_name,
            position=specialist.position,
        )


class SpecialistResponseWithSkills(BaseModel):
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    full_name: str = Field(..., example="Петров Пётр Петрович")
    position: str = Field(..., example="Junior")
    skills: list[str] = Field(..., example=["SQL", "Backend", "Frontend"])

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, specialist: Specialist):
        return cls(
            uuid=specialist.uuid,
            full_name=specialist.full_name,
            position=specialist.position,
            skills=[skill.skill_name for skill in specialist.skills],
        )

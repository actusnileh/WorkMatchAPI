from pydantic import BaseModel


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

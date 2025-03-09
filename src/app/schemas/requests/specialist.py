from pydantic import BaseModel


class CreateSpecialistRequest(BaseModel):
    position: str
    about_me: str
    employment_type_str: str

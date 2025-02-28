from pydantic import (
    BaseModel,
    Field,
)


class CurrentUser(BaseModel):
    o_id: int = Field(None, description="User ID")

    class Config:
        validate_assignment = True

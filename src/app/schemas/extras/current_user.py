from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class CurrentUser(BaseModel):
    o_id: int = Field(None, description="User ID")

    model_config = ConfigDict(validate_assignment=True)

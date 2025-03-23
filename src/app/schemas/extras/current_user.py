from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class CurrentUser(BaseModel):
    o_id: int = Field(default=None, description="User ID", json_schema_extra={"example": 123})

    model_config = ConfigDict(validate_assignment=True)

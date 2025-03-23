from pydantic import (
    BaseModel,
    Field,
)


class Health(BaseModel):
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    status: str = Field(..., json_schema_extra={"example": "OK"})

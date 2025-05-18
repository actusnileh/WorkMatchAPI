from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.models import Application


class AnalysisResponse(BaseModel):
    o_id: int
    specialist_uuid: UUID
    vacancy_uuid: UUID
    match_percentage: float
    mismatches: list

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, application: Application):
        return cls(
            o_id=application.o_id,
            specialist_uuid=application.specialist_uuid,
            vacancy_uuid=application.vacancy_uuid,
            match_percentage=application.match_percentage,
            mismatches=application.mismatches,
        )


class ListAnalysisResponse(BaseModel):
    analysis: list[AnalysisResponse]

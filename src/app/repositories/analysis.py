from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.analysis_result import AnalysisResult
from core.repository import BaseRepository


class AnalysisRepository(BaseRepository[AnalysisResult]):
    async def get_by_specialist_vacancy(self, specialist_uuid: str, vacancy_uuid: str) -> AnalysisResult:
        query = (
            select(AnalysisResult)
            .options(joinedload(AnalysisResult.specialist))
            .filter(
                AnalysisResult.specialist_uuid == specialist_uuid,
                AnalysisResult.vacancy_uuid == vacancy_uuid,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

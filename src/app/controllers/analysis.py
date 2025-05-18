from fastapi import HTTPException, status
from app.models import AnalysisResult
from app.repositories import AnalysisRepository
from core.controller import BaseController


class AnalysisController(BaseController[AnalysisResult]):
    def __init__(self, analysis_repository: AnalysisRepository):
        super().__init__(model=AnalysisResult, repository=analysis_repository)
        self.analysis_repository = analysis_repository

    async def get_by_specialist(self, specialist_uuid: str, vacancy_uuid: str) -> AnalysisResult:
        analysis = await self.analysis_repository.get_by_specialist_vacancy(
            specialist_uuid=specialist_uuid,
            vacancy_uuid=vacancy_uuid,
        )
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Анализ на данную вакансию не найдена.",
            )

        return analysis

    async def get_all_by_specialist(self, specialist_uuid: str) -> list[AnalysisResult]:
        analysis = await self.analysis_repository.get_by(
            field="specialist_uuid",
            value=specialist_uuid,
        )
        return analysis

    async def get_all_by_vacancy(self, vacancy_uuid: str) -> list[AnalysisResult]:
        analysis = await self.analysis_repository.get_by(
            field="vacancy_uuid",
            value=vacancy_uuid,
        )
        return analysis

from app.models import (
    Specialist,
    User,
)
from app.repositories import SpecialistRepository
from core.controller import BaseController
from core.database import Transactional
from src.core.exceptions.base import BadRequestException


class SpecialistController(BaseController[Specialist]):
    def __init__(self, specialist_repository: SpecialistRepository):
        super().__init__(model=Specialist, repository=specialist_repository)
        self.specialist_repository = specialist_repository

    @Transactional()
    async def create_specialist(
        self,
        created_by: User,
        position: str,
        about_me: str,
        employment_type_str: str,
    ) -> Specialist:
        employment_type = await self.specialist_repository.get_employment_type_by_name(
            employment_type_str,
        )
        if not employment_type:
            raise BadRequestException(
                "Указанный тип занятости не найден. Возможные значения: full-time, part-time",
            )

        return await self.specialist_repository.create(
            {
                "created_by": created_by.o_id,
                "full_name": created_by.full_name,
                "position": position,
                "about_me": about_me,
                "employment_type_id": employment_type.o_id,
            },
        )

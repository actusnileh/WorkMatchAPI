from http.client import HTTPException

from fastapi import status

from pydantic import UUID4

from app.models import (
    Specialist,
    User,
)
from app.repositories import SpecialistRepository
from core.controller import BaseController
from core.database import Transactional
from src.core.exceptions.base import BadRequestException
from src.core.utils.datetime_util import utcnow


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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Указанный тип занятости не найден. Возможные значения: full-time, part-time.",
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

    @Transactional()
    async def update_by_uuid(self, user: User, uuid: UUID4, attrs: dict) -> Specialist:
        attrs["updated_at"] = utcnow()
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise BadRequestException("По указанному UUID не найдено резюме")
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для редактирования данного резюме.",
            )

        return await self.specialist_repository._update(specialist, attrs)

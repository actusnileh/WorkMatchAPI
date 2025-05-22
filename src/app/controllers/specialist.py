import re
from datetime import date
from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException

from pydantic import UUID4

from app.models import (
    Specialist,
    User,
)
from app.repositories import SpecialistRepository
from core.controller import BaseController
from core.database import Transactional
from core.exceptions import BadRequestException
from core.utils.datetime_util import utcnow


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

        created_specialist = await self.specialist_repository.create(
            {
                "created_by": created_by.o_id,
                "full_name": created_by.full_name,
                "position": position,
                "about_me": about_me,
                "employment_type_id": employment_type.o_id,
            },
        )
        return created_specialist, employment_type

    async def get_by_uuid(self, uuid: str) -> Specialist:
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        return specialist

    @Transactional()
    async def update_by_uuid(self, user: User, uuid: UUID4, attrs: dict) -> Specialist:
        attrs["updated_at"] = utcnow()

        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для редактирования данного резюме.",
            )

        if "employment_type_str" in attrs:
            employment_type = await self.specialist_repository.get_employment_type_by_name(
                attrs.pop("employment_type_str"),
            )
            if not employment_type:
                raise BadRequestException("Указанный тип занятости не найден.")
            attrs["employment_type"] = employment_type

        updated_specialist = await self.specialist_repository._update(specialist, attrs)
        return updated_specialist

    async def add_skill(self, user: User, uuid: UUID4, skill_name: str) -> Specialist:
        normalized_skill_name = re.sub(r"\s+", " ", skill_name.strip().lower())
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для редактирования данного резюме.",
            )
        existing_skill = next(
            (skill for skill in specialist.skills if skill.skill_name.lower() == normalized_skill_name),
            None,
        )
        if existing_skill:
            return specialist

        return await self.specialist_repository.add_skill(
            specialist,
            normalized_skill_name,
        )

    async def remove_skill(
        self,
        user: User,
        uuid: UUID4,
        skill_name: str,
    ) -> Specialist:
        normalized_skill_name = re.sub(r"\s+", " ", skill_name.strip().lower())
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для редактирования данного резюме.",
            )
        skill_to_remove = next(
            (skill for skill in specialist.skills if skill.skill_name.lower() == normalized_skill_name),
            None,
        )
        if skill_to_remove:
            return await self.specialist_repository.remove_skill(
                skill_to_remove,
                specialist,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не найдено ни одного навыка с указанным именем.",
            )

    async def add_experience(
        self,
        user: User,
        uuid: UUID4,
        company_name: str,
        position: str,
        start_date: date,
        end_date: date,
    ) -> Specialist:
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для редактирования данного резюме.",
            )

        return await self.specialist_repository.add_experience(
            specialist,
            company_name,
            position,
            start_date,
            end_date,
        )

    async def remove_experience(
        self,
        user: User,
        uuid: UUID4,
        experience_uuid: UUID,
    ) -> Specialist:
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для редактирования данного резюме.",
            )
        experience_to_remove = next(
            (exp for exp in specialist.experiences if str(exp.uuid) == str(experience_uuid)),
            None,
        )

        if not experience_to_remove:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Опыт работы с указанным UUID не найден.",
            )
        return await self.specialist_repository.remove_experience(experience_to_remove, specialist)

    async def get_by_user(self, user: User):
        specialists = await self.specialist_repository.get_by(
            field="created_by",
            value=user.o_id,
            join_={"employment_types", "skills", "experience"},
            unique=False,
        )
        if len(specialists) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="У вас нет резюме.",
            )
        return specialists

    async def delete_by_uuid(self, user, uuid: str):
        specialist: Specialist = await self.specialist_repository.get_by_uuid(uuid=uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )
        if user.o_id != specialist.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления данного резюме.",
            )
        await self.specialist_repository.delete(specialist)

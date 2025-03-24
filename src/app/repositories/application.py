from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import Application
from core.repository import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    async def get_by_specialist_vacancy(self, specialist_uuid: str, vacancy_uuid: str) -> Application:
        query = (
            select(Application)
            .options(joinedload(Application.specialist))
            .filter(
                Application.specialist_uuid == specialist_uuid,
                Application.vacancy_uuid == vacancy_uuid,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

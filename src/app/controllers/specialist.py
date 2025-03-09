from app.models import Specialist
from app.repositories import SpecialistRepository
from core.controller import BaseController
from core.database import Transactional


class SpecialistController(BaseController[Specialist]):
    def __init__(self, specialist_repository: SpecialistRepository):
        super().__init__(model=Specialist, repository=specialist_repository)
        self.specialist_repository = specialist_repository

    @Transactional()
    async def create_specialist(
        self,
        external_id: int,
        full_name: str,
        position: str,
    ) -> Specialist:
        pass

from functools import partial

from fastapi import Depends

from app.controllers import (
    AuthController,
    SpecialistController,
    UserController,
    VacancyController,
)
from app.models import (
    Specialist,
    User,
    Vacancy,
)
from app.repositories import (
    SpecialistRepository,
    UserRepository,
    VacancyRepository,
)
from core.database import get_session


class Factory:
    user_repository = partial(UserRepository, User)
    specialist_repository = partial(SpecialistRepository, Specialist)
    vacancy_repository = partial(VacancyRepository, Vacancy)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session),
        )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
        )

    def get_vacancy_controller(self, db_session=Depends(get_session)):
        return VacancyController(
            vacancy_repository=self.vacancy_repository(db_session=db_session),
        )

    def get_specialist_controller(self, db_session=Depends(get_session)):
        return SpecialistController(
            specialist_repository=self.specialist_repository(db_session=db_session),
        )

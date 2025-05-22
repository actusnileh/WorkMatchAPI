from fastapi import Depends

from app.controllers import (
    AnalysisController,
    ApplicationController,
    AuthController,
    SpecialistController,
    UserController,
    VacancyController,
)
from app.models import (
    AnalysisResult,
    Application,
    Specialist,
    User,
    Vacancy,
)
from app.repositories import (
    AnalysisRepository,
    ApplicationRepository,
    SpecialistRepository,
    UserRepository,
    VacancyRepository,
)
from core.database import get_session


class Factory:
    @staticmethod
    def user_repository(db_session):
        return UserRepository(User, db_session)

    @staticmethod
    def specialist_repository(db_session):
        return SpecialistRepository(Specialist, db_session)

    @staticmethod
    def vacancy_repository(db_session):
        return VacancyRepository(Vacancy, db_session)

    @staticmethod
    def application_repository(db_session):
        return ApplicationRepository(Application, db_session)

    @staticmethod
    def analysis_repository(db_session):
        return AnalysisRepository(AnalysisResult, db_session)

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

    def get_application_controller(self, db_session=Depends(get_session)):
        return ApplicationController(
            application_repository=self.application_repository(db_session),
            specialist_repository=self.specialist_repository(db_session),
            vacancy_repository=self.vacancy_repository(db_session),
        )

    def get_analysis_controller(self, db_session=Depends(get_session)):
        return AnalysisController(analysis_repository=self.analysis_repository(db_session))

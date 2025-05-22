from .analysis import AnalysisController
from .application import ApplicationController
from .auth import AuthController
from .specialist import SpecialistController
from .user import UserController
from .vacancy import VacancyController


__all__ = [
    "AuthController",
    "UserController",
    "VacancyController",
    "SpecialistController",
    "ApplicationController",
    "AnalysisController",
]

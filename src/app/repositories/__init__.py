from .application import ApplicationRepository
from .specialist import SpecialistRepository
from .user import UserRepository
from .vacancy import VacancyRepository
from .analysis import AnalysisRepository

__all__ = [
    "UserRepository",
    "VacancyRepository",
    "SpecialistRepository",
    "ApplicationRepository",
    "AnalysisRepository",
]

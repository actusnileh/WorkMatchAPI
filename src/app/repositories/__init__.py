from .application import ApplicationRepository
from .specialist import SpecialistRepository
from .user import UserRepository
from .vacancy import VacancyRepository


__all__ = [
    "UserRepository",
    "VacancyRepository",
    "SpecialistRepository",
    "ApplicationRepository",
]

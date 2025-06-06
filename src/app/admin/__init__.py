from .analysis import AnalysisResultAdmin
from .applications import ApplicationAdmin
from .experience import ExperienceAdmin
from .role import RoleAdmin
from .skill import SkillAdmin
from .specialist import SpecialistAdmin
from .user import UserAdmin
from .vacancy import VacancyAdmin


__all__ = [
    "UserAdmin",
    "VacancyAdmin",
    "SpecialistAdmin",
    "SkillAdmin",
    "ApplicationAdmin",
    "RoleAdmin",
    "ExperienceAdmin",
    "AnalysisResultAdmin",
]

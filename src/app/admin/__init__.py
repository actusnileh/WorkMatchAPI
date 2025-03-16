from .experience import ExperienceAdmin
from .role import RoleAdmin
from .skill import SkillAdmin
from .specialist import SpecialistAdmin
from .user import UserAdmin
from .user_action import UserActionAdmin
from .vacancy import VacancyAdmin


__all__ = [
    "UserAdmin",
    "VacancyAdmin",
    "SpecialistAdmin",
    "SkillAdmin",
    "RoleAdmin",
    "UserActionAdmin",
    "ExperienceAdmin",
]

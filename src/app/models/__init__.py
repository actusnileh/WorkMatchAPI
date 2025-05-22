from core.database import Base

from .analysis_result import AnalysisResult
from .application import Application
from .employment_type import EmploymentType
from .role import Role
from .specialist import Specialist
from .specialist_experience import SpecialistExperience
from .specialist_skill import SpecialistSkill
from .user import User
from .vacancy import Vacancy

__all__ = [
    "Base",
    "AnalysisResult",
    "Application",
    "EmploymentType",
    "Role",
    "Specialist",
    "SpecialistExperience",
    "SpecialistSkill",
    "User",
    "Vacancy",
]

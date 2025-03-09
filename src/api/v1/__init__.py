from fastapi import APIRouter

from .monitoring import monitoring_router
from .specialists import specialists_router
from .users import users_router
from .vacancy import vacancies_router


v1_router = APIRouter()
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(vacancies_router, prefix="/vacancies")
v1_router.include_router(monitoring_router, prefix="/monitoring")

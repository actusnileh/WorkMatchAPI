from fastapi import APIRouter

from .vacancy import vacancy_router


vacancies_router = APIRouter()
vacancies_router.include_router(vacancy_router, tags=["Vacancy"])

__all__ = ["vacancies_router"]

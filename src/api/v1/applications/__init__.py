from fastapi import APIRouter

from .applications import application_router


applications_router = APIRouter()
applications_router.include_router(application_router, tags=["Application"])

__all__ = ["applications_router"]

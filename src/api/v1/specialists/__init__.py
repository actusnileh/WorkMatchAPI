from fastapi import APIRouter

from .specialists import specialist_router


specialists_router = APIRouter()
specialists_router.include_router(specialist_router, tags=["Specialist"])

__all__ = ["specialists_router"]

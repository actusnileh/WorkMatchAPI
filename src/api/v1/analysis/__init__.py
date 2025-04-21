from fastapi import APIRouter

from .analysis import analyse_router


analysis_router = APIRouter()
analysis_router.include_router(analyse_router, tags=["Analysis"])

__all__ = ["analysis_router"]

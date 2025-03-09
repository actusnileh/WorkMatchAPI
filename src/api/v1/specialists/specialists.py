from fastapi import (
    APIRouter,
    Depends,
)

from app.models import User
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from src.core.fastapi.dependencies.role_required import RoleRequired


specialist_router = APIRouter()


@specialist_router.post(
    "/",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=201,
)
async def create_specialist(user: User = Depends(get_current_user)):
    return ""

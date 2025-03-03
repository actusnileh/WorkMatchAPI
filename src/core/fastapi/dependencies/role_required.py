from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.models import User
from core.fastapi.dependencies.current_user import get_current_user


def RoleRequired(required_role: list[str]):
    async def role_required(user: User = Depends(get_current_user)):
        if user.role.name not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Только {[role.upper() for role in required_role]} \
может выполнять это действие.",
            )

    return role_required

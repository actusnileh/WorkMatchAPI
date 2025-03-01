from functools import partial

from fastapi import Depends

from app.controllers import (
    AuthController,
    UserController,
)
from app.models import User
from app.repositories import UserRepository
from core.database import get_session


class Factory:
    user_repository = partial(UserRepository, User)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session),
        )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
        )

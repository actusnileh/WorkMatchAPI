from app.controllers import (
    AuthController,
    UserController,
)
from app.models import User
from app.repositories import UserRepository


class ControllerOverrides:
    def __init__(self, db_session):
        self.db_session = db_session

    def user_controller(self):
        return UserController(UserRepository(model=User, session=self.db_session))

    def auth_controller(self):
        return AuthController(UserRepository(model=User, session=self.db_session))

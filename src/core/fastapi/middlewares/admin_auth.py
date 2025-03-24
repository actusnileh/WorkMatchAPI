from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.models.user import User
from app.repositories.user import UserRepository
from core.database.session import async_session_factory
from core.security.jwt import (
    JWTExpiredError,
    JWTHandler,
)
from core.security.password import PasswordHandler


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with async_session_factory() as db_session:
            user = await UserRepository(
                model=User,
                db_session=db_session,
            ).get_by_username(
                username=username,
                join_={"role"},
            )

            if user and PasswordHandler.verify(user.password, password):
                request.session.update(
                    {
                        "token": JWTHandler.encode(
                            payload={"user_id": user.o_id, "role": user.role.name},
                        ),
                    },
                )
                return True
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        try:
            token = JWTHandler.decode(token)
        except JWTExpiredError:
            request.session.clear()
            return False
        if token["role"] != "admin":
            return False

        return True


authentication_backend = AdminAuth(secret_key="...")

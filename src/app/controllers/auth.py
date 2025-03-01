from pydantic import EmailStr

from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from core.controller import BaseController
from core.database import Transactional
from core.exceptions import (
    BadRequestException,
    UnauthorizedException,
)
from core.security.jwt import JWTHandler
from core.security.password import PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    @Transactional()
    async def register(
        self,
        email: EmailStr,
        password: str,
        username: str,
        full_name: str,
    ) -> User:
        user = await self.user_repository.get_by_email(email)

        if user:
            raise BadRequestException("Пользователь с таким email уже зарегистрирован")

        user = await self.user_repository.get_by_username(username)

        if user:
            raise BadRequestException(
                "Пользователь с таким username уже зарегистрирован",
            )

        password = PasswordHandler.password_hash(password)

        return await self.user_repository.create(
            {
                "email": email,
                "password": password,
                "username": username,
                "full_name": full_name,
            },
        )

    async def login(self, email: EmailStr, password: str) -> Token:
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise BadRequestException("Invalid credentials")

        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException("Invalid credentials")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": user.o_id}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

    async def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        token = JWTHandler.decode(access_token)
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

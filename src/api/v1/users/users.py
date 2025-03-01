from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import (
    AuthController,
)
from app.models.user import (
    User,
)
from app.schemas.extras.token import Token
from app.schemas.requests.users import (
    LoginUserRequest,
    RegisterUserRequest,
)
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user


user_router = APIRouter()


@user_router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
        full_name=register_user_request.full_name,
        role_str=register_user_request.role.value,
        employment_type_str=register_user_request.employment_type.value,
    )


@user_router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email,
        password=login_user_request.password,
    )


@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    user = user[0]
    return UserResponse.from_orm_instance(user)

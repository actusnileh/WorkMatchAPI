from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import (
    AuthController,
    UserController,
)
from app.models.user import User
from app.schemas.extras.token import Token
from app.schemas.requests.users import (
    EditPasswordRequest,
    EditUserRequest,
    LoginUserRequest,
    RegisterUserRequest,
)
from app.schemas.responses.users import (
    RegisterUserResponse,
    UserResponse,
)
from core.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user


user_router = APIRouter()


@user_router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> RegisterUserResponse:
    user: User = await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
        full_name=register_user_request.full_name,
        role_str=register_user_request.role.value,
    )
    return RegisterUserResponse.from_orm(user)


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
    return UserResponse.from_orm(user)


@user_router.patch("/edit", dependencies=[Depends(AuthenticationRequired)])
async def edit_user(
    edit_user_request: EditUserRequest,
    user: User = Depends(get_current_user),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    updated_user = await user_controller.update_by_user(
        user=user,
        attrs=edit_user_request.model_dump(exclude_unset=True),
    )
    return UserResponse.from_orm(updated_user)


@user_router.patch("/edit/password", dependencies=[Depends(AuthenticationRequired)])
async def edit_user_password(
    edit_password_request: EditPasswordRequest,
    user: User = Depends(get_current_user),
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    updated_user = await auth_controller.update_password(
        user,
        edit_password_request.old_password,
        edit_password_request.new_password,
    )
    return UserResponse.from_orm(updated_user)

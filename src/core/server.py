from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqladmin import Admin

from api import router
from app.admin import (
    ExperienceAdmin,
    RoleAdmin,
    SkillAdmin,
    SpecialistAdmin,
    UserAdmin,
    VacancyAdmin,
)
from core.config import config
from core.database.session import engines
from core.exceptions import CustomException
from core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
)
from core.cache import Cache, CustomKeyMaker, RedisBackend
from core.fastapi.middlewares.admin_auth import authentication_backend


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="WorkMatchAPI",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()

    admin = Admin(
        app_,
        engines["writer"],
        authentication_backend=authentication_backend,
    )
    admin.add_view(UserAdmin)
    admin.add_view(VacancyAdmin)
    admin.add_view(SpecialistAdmin)
    admin.add_view(SkillAdmin)
    admin.add_view(RoleAdmin)
    admin.add_view(ExperienceAdmin)

    return app_


app = create_app()

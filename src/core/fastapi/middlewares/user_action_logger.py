from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from core.database.standalone_session import standalone_session
from app.models import UserAction
from app.schemas.extras.current_user import CurrentUser
from src.core.database.session import async_session_factory


class UserActionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @standalone_session
    async def log_user_action(
        self, user_id: int, action: str, action_type: str, target_id: int | None
    ):
        async with async_session_factory() as db_session:
            user_action = UserAction(
                user_id=user_id,
                action=action,
                target_id=target_id,
                target_type=action_type,
            )
            db_session.add(user_action)
            await db_session.commit()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive)
            user = scope.get("user")
            user_id = user.o_id if isinstance(user, CurrentUser) else None

            target_id = None
            if "target_id" in request.query_params:
                target_id = int(request.query_params["target_id"])
            elif "target_id" in request.path_params:
                target_id = int(request.path_params["target_id"])

            if user_id:
                await self.log_user_action(
                    user_id=user_id,
                    action=request.url.path,
                    action_type=request.method,
                    target_id=target_id,
                )

        await self.app(scope, receive, send)

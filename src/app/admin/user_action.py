from sqladmin import ModelView

from app.models import UserAction


class UserActionAdmin(ModelView, model=UserAction):
    column_list = [UserAction.o_id, UserAction.user_id, UserAction.action, UserAction.target_type]
    name = "Действие"
    name_plural = "Действия"
    icon = "fa-solid fa-location-dot"

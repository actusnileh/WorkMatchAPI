from sqladmin import ModelView

from app.models import Role


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.o_id, Role.name]
    name = "Роль"
    name_plural = "Роли"
    icon = "fa-solid fa-user-tie"

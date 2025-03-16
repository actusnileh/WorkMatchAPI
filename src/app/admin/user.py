from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.o_id, User.username, User.role]
    column_details_exclude_list = [User.password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

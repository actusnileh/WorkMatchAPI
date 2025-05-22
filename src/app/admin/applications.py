from sqladmin import ModelView

from app.models import Application


class ApplicationAdmin(ModelView, model=Application):
    column_list = [
        Application.o_id,
        Application.specialist,
        Application.vacancy,
        Application.applied,
    ]
    name = "Отклик"
    name_plural = "Отклики"
    icon = "fa-solid fa-bell"

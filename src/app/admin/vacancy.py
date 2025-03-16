from sqladmin import ModelView

from app.models import Vacancy


class VacancyAdmin(ModelView, model=Vacancy):
    column_list = [Vacancy.o_id, Vacancy.title]
    name = "Вакансия"
    name_plural = "Вакансии"
    icon = "fa-solid fa-list"

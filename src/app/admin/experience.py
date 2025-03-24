from sqladmin import ModelView

from app.models import SpecialistExperience


class ExperienceAdmin(ModelView, model=SpecialistExperience):
    column_list = [SpecialistExperience.o_id, SpecialistExperience.company_name]
    name = "Опыт"
    name_plural = "Опыты"
    icon = "fa-solid fa-briefcase"

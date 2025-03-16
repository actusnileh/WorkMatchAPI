from sqladmin import ModelView

from app.models import SpecialistExperience


class ExperienceAdmin(ModelView, model=SpecialistExperience):
    column_list = [SpecialistExperience.o_id, SpecialistExperience.company_name]
    name = "Опыт"
    icon = "fa-solid fa-briefcase"

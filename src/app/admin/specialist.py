from sqladmin import ModelView

from app.models import Specialist


class SpecialistAdmin(ModelView, model=Specialist):
    column_list = [Specialist.o_id, Specialist.full_name, Specialist.uuid]
    name = "Специалист"
    name_plural = "Специалисты"
    icon = "fa-solid fa-envelope"

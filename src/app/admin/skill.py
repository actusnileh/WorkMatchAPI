from sqladmin import ModelView

from app.models import SpecialistSkill


class SkillAdmin(ModelView, model=SpecialistSkill):
    column_list = [SpecialistSkill.o_id, SpecialistSkill.skill_name]
    name = "Скилл"
    name_plural = "Скиллы"
    icon = "fa-solid fa-book"

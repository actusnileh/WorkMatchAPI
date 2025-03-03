from pydantic import (
    BaseModel,
    Field,
)


class VacancyResponse(BaseModel):
    title: str = Field(..., example="Инженер по стандартизации/нормоконтроль")
    description: str = Field(
        ...,
        example="Нейробанк - государственная ИТ-организация, работающая в сфере финтеха более 30 лет.",
    )
    requirements: str = Field(
        ...,
        example="Профильное образование специальностям или повышение\
квалификации 'Менеджмент качества', 'Стандартизация', 'Сертификация' и т.п.;",
    )
    conditions: str = Field(
        ...,
        example="Опыт работы: 1–3 года; Полная занятость; График: 5/2; Рабочие часы: 8",
    )
    employment_type: str = Field(..., example="full-time")

    class Config:
        from_attributes = True

from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    UUID4,
)


class VacancyResponse(BaseModel):
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
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
    salary: PositiveFloat = Field(..., example="65000")
    employment_type: str = Field(..., example="full-time")

    class Config:
        from_attributes = True

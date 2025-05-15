from sqladmin import ModelView

from app.models import AnalysisResult


class AnalysisResultAdmin(ModelView, model=AnalysisResult):
    column_list = [
        AnalysisResult.o_id,
        AnalysisResult.match_percentage,
        AnalysisResult.mismatches,
        AnalysisResult.specialist,
        AnalysisResult.vacancy,
    ]
    name = "Результат анализа"
    name_plural = "Результаты анализа"
    icon = "fa-solid fa-magnifying-glass-chart"

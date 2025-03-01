from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class AnalysisResult(Base, TimestampMixin):
    __tablename__ = "analysis_results"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    vacancy_id = Column(BigInteger, ForeignKey("vacancies.o_id"), nullable=False)
    specialist_id = Column(BigInteger, ForeignKey("specialists.o_id"), nullable=False)
    match_percentage = Column(Numeric(5, 2), nullable=False)
    mismatches = Column(Text)

    vacancy = relationship("Vacancy")
    specialist = relationship("Specialist")

    __mapper_args__ = {"eager_defaults": True}

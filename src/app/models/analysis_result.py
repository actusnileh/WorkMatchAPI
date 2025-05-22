from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Numeric,
    Text,
    UUID,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class AnalysisResult(Base, TimestampMixin):
    __tablename__ = "analysis_results"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    vacancy_uuid = Column(UUID, ForeignKey("vacancies.uuid", ondelete="CASCADE"), nullable=False)
    specialist_uuid = Column(UUID, ForeignKey("specialists.uuid", ondelete="CASCADE"), nullable=False)
    match_percentage = Column(Numeric(5, 2), nullable=False)
    mismatches = Column(ARRAY(Text))

    vacancy = relationship("Vacancy", back_populates="analysis_results")
    specialist = relationship("Specialist", back_populates="analysis_results")

    __mapper_args__ = {"eager_defaults": True}

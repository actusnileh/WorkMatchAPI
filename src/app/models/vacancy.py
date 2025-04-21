from uuid import uuid4

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    ForeignKey,
    TEXT,
    Unicode,
    UUID,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class Vacancy(Base, TimestampMixin):
    __tablename__ = "vacancies"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    title = Column(Unicode(255), nullable=False)
    description = Column(TEXT, nullable=False)
    requirements = Column(TEXT, nullable=False)
    conditions = Column(TEXT, nullable=False)
    salary = Column(BigInteger, nullable=False)
    employment_type_id = Column(
        BigInteger,
        ForeignKey("employment_types.o_id", ondelete="CASCADE"),
        nullable=True,
    )
    created_by = Column(BigInteger, ForeignKey("users.o_id"), nullable=False)

    creator = relationship("User", back_populates="vacancies")
    employment_type = relationship("EmploymentType", back_populates="vacancies")
    applications = relationship("Application", back_populates="vacancy")
    analysis_results = relationship("AnalysisResult", back_populates="vacancy", cascade="all, delete-orphan")

    CheckConstraint("salary > 0", name="check_salary_positive")

    __mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f"{self.title}"

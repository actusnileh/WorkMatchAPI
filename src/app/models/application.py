from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.utils import utcnow


class ApplicationStatus(Base):
    __tablename__ = "application_statuses"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)

    applications = relationship("Application", back_populates="status")


class Application(Base):
    __tablename__ = "applications"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    specialist_id = Column(BigInteger, ForeignKey("specialists.o_id"), nullable=False)
    vacancy_id = Column(BigInteger, ForeignKey("vacancies.o_id"), nullable=False)
    status_id = Column(BigInteger, ForeignKey("application_statuses.o_id"), nullable=False)
    applied_at = Column(DateTime, default=utcnow, nullable=False)

    specialist = relationship("Specialist", back_populates="applications")
    vacancy = relationship("Vacancy", back_populates="applications")
    status = relationship("ApplicationStatus", back_populates="applications")

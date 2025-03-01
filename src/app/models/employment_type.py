from sqlalchemy import (
    BigInteger,
    Column,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base


class EmploymentType(Base):
    __tablename__ = "employment_types"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)

    users = relationship("User", back_populates="employment_type")
    vacancies = relationship("Vacancy", back_populates="employment_type")
    __mapper_args__ = {"eager_defaults": True}

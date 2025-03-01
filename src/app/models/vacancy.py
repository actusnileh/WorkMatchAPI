from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    TEXT,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class Vacancy(Base, TimestampMixin):
    __tablename__ = "vacancies"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(Unicode(255), nullable=False)
    description = Column(TEXT, nullable=False)
    requirements = Column(TEXT, nullable=False)
    conditions = Column(TEXT, nullable=False)
    employment_type_id = Column(
        BigInteger,
        ForeignKey("employment_types.o_id"),
        nullable=True,
    )
    created_by = Column(BigInteger, ForeignKey("users.o_id"), nullable=False)

    creator = relationship("User", back_populates="vacancies")
    employment_type = relationship("EmploymentType", back_populates="vacancies")

    __mapper_args__ = {"eager_defaults": True}

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base


class SpecialistExperience(Base):
    __tablename__ = "specialist_experience"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    specialist_id = Column(BigInteger, ForeignKey("specialists.o_id"), nullable=False)
    company_name = Column(Unicode(255))
    position = Column(Unicode(255))
    start_date = Column(Date)
    end_date = Column(Date)

    specialist = relationship("Specialist", back_populates="experiences")

    __mapper_args__ = {"eager_defaults": True}

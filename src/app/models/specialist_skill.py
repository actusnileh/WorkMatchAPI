from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

from core.database import Base


class SpecialistSkill(Base):
    __tablename__ = "specialist_skills"

    specialist_id = Column(BigInteger, ForeignKey("specialists.o_id"), primary_key=True)
    skill_name = Column(String)

    specialist = relationship("Specialist", back_populates="skills")

    __mapper_args__ = {"eager_defaults": True}

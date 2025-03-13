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

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)

    specialist_id = Column(BigInteger, ForeignKey("specialists.o_id"))
    skill_name = Column(String)

    specialist = relationship("Specialist", back_populates="skills")

    __mapper_args__ = {"eager_defaults": True}

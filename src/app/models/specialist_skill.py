from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class SpecialistSkill(Base, TimestampMixin):
    __tablename__ = "specialist_skills"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)

    specialist_id = Column(BigInteger, ForeignKey("specialists.o_id", ondelete="CASCADE"))
    skill_name = Column(String)

    specialist = relationship("Specialist", back_populates="skills")

    __mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f"{self.skill_name}"

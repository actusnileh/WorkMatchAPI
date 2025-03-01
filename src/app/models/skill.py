from sqlalchemy import (
    BigInteger,
    Column,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)

    specialists = relationship("SpecialistSkill", back_populates="skill")

    __mapper_args__ = {"eager_defaults": True}

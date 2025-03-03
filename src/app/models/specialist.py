from uuid import uuid4

from sqlalchemy import (
    BigInteger,
    Column,
    Unicode,
    UUID,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class Specialist(Base, TimestampMixin):
    __tablename__ = "specialists"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    external_id = Column(Unicode(255), unique=True, nullable=False)
    full_name = Column(Unicode(255), nullable=False)
    position = Column(Unicode(255))

    skills = relationship("SpecialistSkill", back_populates="specialist")
    experiences = relationship("SpecialistExperience", back_populates="specialist")

    __mapper_args__ = {"eager_defaults": True}

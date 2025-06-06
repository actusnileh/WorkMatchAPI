from uuid import uuid4

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Text,
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
    created_by = Column(
        BigInteger,
        ForeignKey("users.o_id", ondelete="CASCADE"),
        nullable=False,
    )
    full_name = Column(Unicode(255), nullable=False)
    about_me = Column(Text)
    position = Column(Unicode(255))
    employment_type_id = Column(
        BigInteger,
        ForeignKey("employment_types.o_id", ondelete="CASCADE"),
        nullable=True,
    )

    employment_type = relationship("EmploymentType", back_populates="specialist")
    creator = relationship("User", back_populates="specialist")
    skills = relationship("SpecialistSkill", back_populates="specialist")
    experiences = relationship("SpecialistExperience", back_populates="specialist")
    applications = relationship("Application", back_populates="specialist")
    analysis_results = relationship("AnalysisResult", back_populates="specialist", cascade="all, delete-orphan")

    __mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f"{self.full_name}"

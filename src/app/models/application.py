from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    UniqueConstraint,
    UUID,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class Application(Base, TimestampMixin):
    __tablename__ = "applications"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    specialist_uuid = Column(
        UUID,
        ForeignKey(
            "specialists.uuid",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    vacancy_uuid = Column(
        UUID,
        ForeignKey(
            "vacancies.uuid",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    applied = Column(Boolean, default=False, nullable=False)

    specialist = relationship("Specialist", back_populates="applications")
    vacancy = relationship("Vacancy", back_populates="applications")

    __table_args__ = (UniqueConstraint("specialist_uuid", "vacancy_uuid", name="uq_specialist_vacancy"),)

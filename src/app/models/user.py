from uuid import uuid4

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Unicode,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)
    username = Column(Unicode(255), nullable=False, unique=True)
    full_name = Column(Unicode(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(BigInteger, ForeignKey("roles.o_id"), nullable=False)

    role = relationship("Role", back_populates="users")
    vacancies = relationship("Vacancy", back_populates="creator")
    specialist = relationship("Specialist", back_populates="creator")

    __mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f"Пользователь #{self.username}"

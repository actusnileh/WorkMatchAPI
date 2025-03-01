from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum

from core.database import Base


class RoleName(Enum):
    HR = "hr"
    ADMIN = "admin"
    USER = "user"


class Role(Base):
    __tablename__ = "roles"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(SQLAlchemyEnum(RoleName), nullable=False, unique=True)
    users = relationship("User", back_populates="role")

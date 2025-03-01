from sqlalchemy import (
    BigInteger,
    Column,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base


class Role(Base):
    __tablename__ = "roles"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, unique=True)
    users = relationship("User", back_populates="role")

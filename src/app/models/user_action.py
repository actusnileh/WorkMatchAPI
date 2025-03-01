from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    func,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class UserAction(Base, TimestampMixin):
    __tablename__ = "user_actions"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.o_id"), nullable=False)
    action = Column(Unicode(255), nullable=False)
    target_id = Column(BigInteger)
    target_type = Column(Unicode(50))
    timestamp = Column(DateTime, default=func.now())

    user = relationship("User")

    __mapper_args__ = {"eager_defaults": True}

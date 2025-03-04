from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Unicode,
)
from sqlalchemy.orm import relationship

from core.database import Base
from core.utils import utcnow


class UserAction(Base):
    __tablename__ = "user_actions"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.o_id"), nullable=False)
    action = Column(Unicode(255), nullable=False)
    target_id = Column(BigInteger)
    target_type = Column(Unicode(50))
    timestamp = Column(DateTime, default=utcnow())

    user = relationship("User")

    __mapper_args__ = {"eager_defaults": True}

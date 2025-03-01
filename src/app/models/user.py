from enum import Enum
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
from core.security.access_control import (
    Allow,
    Everyone,
    RolePrincipal,
    UserPrincipal,
)


class UserPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    o_id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)
    username = Column(Unicode(255), nullable=False, unique=True)
    full_name = Column(Unicode(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role_id = Column(BigInteger, ForeignKey("roles.o_id"), nullable=True)
    employment_type_id = Column(
        BigInteger,
        ForeignKey("employment_types.o_id"),
        nullable=True,
    )

    role = relationship("Role", back_populates="users")
    employment_type = relationship("EmploymentType", back_populates="users")
    vacancies = relationship("Vacancy", back_populates="creator")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [UserPermission.READ, UserPermission.CREATE]
        self_permissions = [
            UserPermission.READ,
            UserPermission.EDIT,
            UserPermission.CREATE,
        ]
        all_permissions = list(UserPermission)

        return [
            (Allow, Everyone, basic_permissions),
            (Allow, UserPrincipal(value=self.o_id), self_permissions),
            (Allow, RolePrincipal(value="admin"), all_permissions),
        ]

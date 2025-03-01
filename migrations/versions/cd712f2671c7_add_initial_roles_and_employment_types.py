"""add initial roles and employment_types

Revision ID: cd712f2671c7
Revises: 81c1e3cf0013
Create Date: 2025-03-01 14:36:09.291218

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

from src.app.models import Role, EmploymentType
from src.app.models.role import RoleName


# revision identifiers, used by Alembic.
revision: str = "cd712f2671c7"
down_revision: Union[str, None] = "81c1e3cf0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # Создаем записи для ролей
    roles = [
        Role(name=RoleName.HR),
        Role(name=RoleName.ADMIN),
        Role(name=RoleName.USER),
    ]

    employment_types = [
        EmploymentType(name="full-time"),
        EmploymentType(name="part-time"),
    ]

    session.add_all(roles)
    session.add_all(employment_types)
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(Role).filter(
        Role.name.in_(
            [
                RoleName.HR,
                RoleName.ADMIN,
                RoleName.USER,
            ]
        )
    ).delete()
    session.query(EmploymentType).filter(
        EmploymentType.name.in_(
            [
                "part-time",
                "full-time",
            ]
        )
    ).delete()
    session.commit()

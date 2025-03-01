"""add initial roles and employment_types

Revision ID: 49b647b6ff17
Revises: 81c1e3cf0013
Create Date: 2025-03-01 17:21:55.729151

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "49b647b6ff17"
down_revision: Union[str, None] = "81c1e3cf0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("name", sa.String),
        ),
        [
            {"name": "hr"},
            {"name": "admin"},
            {"name": "user"},
        ],
    )
    op.bulk_insert(
        sa.table(
            "employment_types",
            sa.column("name", sa.String),
        ),
        [
            {"name": "full-time"},
            {"name": "part-time"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name IN ('HR', 'ADMIN', 'USER')")
    op.execute("DELETE FROM employment_types WHERE name IN ('full-time', 'part-time')")

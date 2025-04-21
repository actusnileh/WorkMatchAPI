"""empty message

Revision ID: 21d53abc8ca3
Revises: 9373a4191fa6
Create Date: 2025-04-21 17:45:21.721302

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "21d53abc8ca3"
down_revision: Union[str, None] = "9373a4191fa6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("name", sa.Unicode),
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
            sa.column("name", sa.Unicode),
        ),
        [
            {"name": "full-time"},
            {"name": "part-time"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name IN ('HR', 'ADMIN', 'USER')")
    op.execute("DELETE FROM employment_types WHERE name IN ('full-time', 'part-time')")

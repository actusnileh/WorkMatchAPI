"""empty message

Revision ID: 137b8a56819f
Revises: 4f0bfa824380
Create Date: 2025-03-23 14:20:12.521383

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "137b8a56819f"
down_revision: Union[str, None] = "4f0bfa824380"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_actions")
    op.alter_column("users", "role_id", existing_type=sa.BIGINT(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "role_id", existing_type=sa.BIGINT(), nullable=True)
    op.create_table(
        "user_actions",
        sa.Column("o_id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("action", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column("target_id", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column("target_type", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("timestamp", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.o_id"], name="user_actions_user_id_fkey"),
        sa.PrimaryKeyConstraint("o_id", name="user_actions_pkey"),
    )
    # ### end Alembic commands ###

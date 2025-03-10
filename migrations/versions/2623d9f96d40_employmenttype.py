"""EmploymentType

Revision ID: 2623d9f96d40
Revises: b4454969cd5a
Create Date: 2025-03-09 16:19:21.080777

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2623d9f96d40"
down_revision: Union[str, None] = "b4454969cd5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("specialists", sa.Column("about_me", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("specialists", "about_me")
    # ### end Alembic commands ###

"""empty message

Revision ID: 823a9133d42a
Revises: 1ba5316e425d
Create Date: 2025-03-16 14:58:22.734372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '823a9133d42a'
down_revision: Union[str, None] = '1ba5316e425d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('specialist_experience', sa.Column('uuid', sa.UUID(), nullable=False))
    op.create_unique_constraint(None, 'specialist_experience', ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'specialist_experience', type_='unique')
    op.drop_column('specialist_experience', 'uuid')
    # ### end Alembic commands ###

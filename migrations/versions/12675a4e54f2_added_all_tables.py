"""Added all tables

Revision ID: 12675a4e54f2
Revises: 5da9f21fca9e
Create Date: 2025-03-01 10:57:12.472539

"""

from typing import (
    Sequence,
    Union,
)

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "12675a4e54f2"
down_revision: Union[str, None] = "5da9f21fca9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "employment_types",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.Unicode(length=50), nullable=False),
        sa.PrimaryKeyConstraint("o_id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "roles",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.Unicode(length=50), nullable=False),
        sa.PrimaryKeyConstraint("o_id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "skills",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.PrimaryKeyConstraint("o_id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "specialists",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("external_id", sa.Unicode(length=255), nullable=False),
        sa.Column("full_name", sa.Unicode(length=255), nullable=False),
        sa.Column("position", sa.Unicode(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("o_id"),
        sa.UniqueConstraint("external_id"),
    )
    op.create_table(
        "specialist_experience",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("specialist_id", sa.BigInteger(), nullable=False),
        sa.Column("company_name", sa.Unicode(length=255), nullable=True),
        sa.Column("position", sa.Unicode(length=255), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["specialist_id"],
            ["specialists.o_id"],
        ),
        sa.PrimaryKeyConstraint("o_id"),
    )
    op.create_table(
        "specialist_skills",
        sa.Column("specialist_id", sa.BigInteger(), nullable=False),
        sa.Column("skill_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.o_id"],
        ),
        sa.ForeignKeyConstraint(
            ["specialist_id"],
            ["specialists.o_id"],
        ),
        sa.PrimaryKeyConstraint("specialist_id", "skill_id"),
    )
    op.create_table(
        "user_actions",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("action", sa.Unicode(length=255), nullable=False),
        sa.Column("target_id", sa.BigInteger(), nullable=True),
        sa.Column("target_type", sa.Unicode(length=50), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.o_id"],
        ),
        sa.PrimaryKeyConstraint("o_id"),
    )
    op.create_table(
        "vacancies",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.Unicode(length=255), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=False),
        sa.Column("requirements", sa.TEXT(), nullable=False),
        sa.Column("conditions", sa.TEXT(), nullable=False),
        sa.Column("employment_type_id", sa.BigInteger(), nullable=True),
        sa.Column("created_by", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.o_id"],
        ),
        sa.ForeignKeyConstraint(
            ["employment_type_id"],
            ["employment_types.o_id"],
        ),
        sa.PrimaryKeyConstraint("o_id"),
    )
    op.create_table(
        "analysis_results",
        sa.Column("o_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("vacancy_id", sa.BigInteger(), nullable=False),
        sa.Column("specialist_id", sa.BigInteger(), nullable=False),
        sa.Column("match_percentage", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("mismatches", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["specialist_id"],
            ["specialists.o_id"],
        ),
        sa.ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancies.o_id"],
        ),
        sa.PrimaryKeyConstraint("o_id"),
    )
    op.add_column(
        "users",
        sa.Column("full_name", sa.Unicode(length=255), nullable=False),
    )
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.add_column("users", sa.Column("role_id", sa.BigInteger(), nullable=True))
    op.add_column(
        "users",
        sa.Column("employment_type_id", sa.BigInteger(), nullable=True),
    )
    op.create_foreign_key(
        None,
        "users",
        "employment_types",
        ["employment_type_id"],
        ["o_id"],
    )
    op.create_foreign_key(None, "users", "roles", ["role_id"], ["o_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "employment_type_id")
    op.drop_column("users", "role_id")
    op.drop_column("users", "is_active")
    op.drop_column("users", "full_name")
    op.drop_table("analysis_results")
    op.drop_table("vacancies")
    op.drop_table("user_actions")
    op.drop_table("specialist_skills")
    op.drop_table("specialist_experience")
    op.drop_table("specialists")
    op.drop_table("skills")
    op.drop_table("roles")
    op.drop_table("employment_types")
    # ### end Alembic commands ###

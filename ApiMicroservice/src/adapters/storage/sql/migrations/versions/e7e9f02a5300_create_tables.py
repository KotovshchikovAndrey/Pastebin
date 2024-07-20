"""create tables

Revision ID: e7e9f02a5300
Revises: 
Create Date: 2024-07-16 10:41:58.381430

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7e9f02a5300"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "category",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('UTC', NOW())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "paste",
        sa.Column("title", sa.String(length=30), nullable=False),
        sa.Column("slug", sa.String(length=8), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("password", sa.String(length=50), nullable=True),
        sa.Column("expired_at", sa.DateTime(), nullable=True),
        sa.Column(
            "drop_after_read", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.Column(
            "views",
            sa.Numeric(precision=10, scale=0),
            server_default="0",
            nullable=False,
        ),
        sa.Column("category_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('UTC', NOW())"),
            nullable=False,
        ),
        sa.CheckConstraint("expired_at > created_at", name="check_expired_at"),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("paste")
    op.drop_table("category")
    # ### end Alembic commands ###

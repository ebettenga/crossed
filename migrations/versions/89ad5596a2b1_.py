"""empty message

Revision ID: 89ad5596a2b1
Revises: 573b3e0498d0
Create Date: 2023-02-16 13:52:38.219254

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "89ad5596a2b1"
down_revision = "573b3e0498d0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "crosswords",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("clues", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("answers", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("circles", sa.ARRAY(sa.Integer()), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("dow", sa.String(), nullable=True),
        sa.Column("grid", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("gridnums", sa.ARRAY(sa.Integer()), nullable=True),
        sa.Column("shadecircles", sa.Boolean(), nullable=True),
        sa.Column("col_size", sa.Integer(), nullable=True),
        sa.Column("row_size", sa.Integer(), nullable=True),
        sa.Column("jnote", sa.String(), nullable=True),
        sa.Column("notepad", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("crosswords")
    # ### end Alembic commands ###

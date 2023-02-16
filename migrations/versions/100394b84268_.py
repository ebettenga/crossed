"""empty message

Revision ID: 100394b84268
Revises: 89ad5596a2b1
Create Date: 2023-02-16 15:04:50.083353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "100394b84268"
down_revision = "89ad5596a2b1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("results")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "results",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("url", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "result_all",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "result_no_stop_words",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="results_pkey"),
    )
    # ### end Alembic commands ###

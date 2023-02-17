"""empty message

Revision ID: e478bb8c519e
Revises: 8d6d215b7a92
Create Date: 2023-02-16 17:24:58.560405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e478bb8c519e"
down_revision = "8d6d215b7a92"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("rooms", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "join_id", sa.Integer(), sa.Identity(always=False), nullable=False
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("rooms", schema=None) as batch_op:
        batch_op.drop_column("join_id")

    # ### end Alembic commands ###

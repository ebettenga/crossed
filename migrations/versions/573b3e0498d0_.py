"""empty message

Revision ID: 573b3e0498d0
Revises: c2c3e698e15b
Create Date: 2023-02-14 13:44:51.450044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '573b3e0498d0'
down_revision = 'c2c3e698e15b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('profile_image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###

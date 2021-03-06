"""'add'

Revision ID: 378050ad4d15
Revises: 1ea74dd7e98c
Create Date: 2018-12-24 14:16:24.252305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '378050ad4d15'
down_revision = '1ea74dd7e98c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Powers', sa.Column('power_hidden', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Powers', 'power_hidden')
    # ### end Alembic commands ###

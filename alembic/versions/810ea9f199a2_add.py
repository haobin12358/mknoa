"""'add'

Revision ID: 810ea9f199a2
Revises: 9c709e6afcc0
Create Date: 2019-01-06 16:58:23.875660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '810ea9f199a2'
down_revision = '9c709e6afcc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ApprovalSov', sa.Column('approvalsov_mouldtime', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ApprovalSov', 'approvalsov_mouldtime')
    # ### end Alembic commands ###

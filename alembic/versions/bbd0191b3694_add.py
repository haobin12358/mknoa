"""'add'

Revision ID: bbd0191b3694
Revises: 810ea9f199a2
Create Date: 2019-01-07 01:44:19.331725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbd0191b3694'
down_revision = '810ea9f199a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('NoticeRead',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('noticeread_id', sa.String(length=64), nullable=False),
    sa.Column('notice_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('is_read', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('noticeread_id')
    )
    op.add_column('Notice', sa.Column('tag_id', sa.Text(), nullable=True))
    op.add_column('Notice', sa.Column('user_id', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Notice', 'user_id')
    op.drop_column('Notice', 'tag_id')
    op.drop_table('NoticeRead')
    # ### end Alembic commands ###

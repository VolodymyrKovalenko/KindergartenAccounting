"""empty message

Revision ID: bb3e431b7874
Revises: 53484903bbc9
Create Date: 2017-12-21 22:11:21.494216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb3e431b7874'
down_revision = '53484903bbc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('report_visits', sa.Column('payment_sum', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('report_visits', 'payment_sum')
    # ### end Alembic commands ###

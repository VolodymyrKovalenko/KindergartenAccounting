"""empty message

Revision ID: 53484903bbc9
Revises: a9c416fea0ac
Create Date: 2017-12-21 18:27:13.953797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53484903bbc9'
down_revision = 'a9c416fea0ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kindergarten', sa.Column('price', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('kindergarten', 'price')
    # ### end Alembic commands ###

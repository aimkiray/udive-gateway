"""empty message

Revision ID: cefc3a449ef0
Revises: 7ddfa62e73b3
Create Date: 2019-01-06 23:59:38.601731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cefc3a449ef0'
down_revision = '7ddfa62e73b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gate', sa.Column('answer_raw', sa.Text(), nullable=True))
    op.add_column('gate', sa.Column('topic_raw', sa.Text(), nullable=True))
    op.drop_column('gate', 'detail_topic')
    op.drop_column('gate', 'detail_answer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gate', sa.Column('detail_answer', mysql.TEXT(), nullable=True))
    op.add_column('gate', sa.Column('detail_topic', mysql.TEXT(), nullable=True))
    op.drop_column('gate', 'topic_raw')
    op.drop_column('gate', 'answer_raw')
    # ### end Alembic commands ###
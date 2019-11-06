"""pic

Revision ID: 66fe6d77807a
Revises: cefc3a449ef0
Create Date: 2019-01-07 02:40:17.236376

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '66fe6d77807a'
down_revision = 'cefc3a449ef0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gate', sa.Column('related_pic', sa.String(length=255), nullable=True))
    op.drop_column('gate', 'common')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gate', sa.Column('common', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('gate', 'related_pic')
    # ### end Alembic commands ###

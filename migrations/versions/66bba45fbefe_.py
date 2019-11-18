"""empty message

Revision ID: 66bba45fbefe
Revises: eb0e88b53190
Create Date: 2019-11-18 15:52:06.801863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66bba45fbefe'
down_revision = 'eb0e88b53190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('gmt_create', sa.DateTime(), nullable=True),
    sa.Column('gmt_modified', sa.DateTime(), nullable=True),
    sa.Column('sensor_type', sa.String(length=100), nullable=True),
    sa.Column('min_value', sa.String(length=100), nullable=True),
    sa.Column('max_value', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('config')
    # ### end Alembic commands ###

"""Retry: add nullable company_id to review

Revision ID: 99d1ff99902a
Revises: ef2fdf5c59c1
Create Date: 2025-03-29 02:06:27.728709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99d1ff99902a'
down_revision = 'ef2fdf5c59c1'
branch_labels = None
depends_on = None


revision = '99d1ff99902a'
down_revision = 'ef2fdf5c59c1'
branch_labels = None
depends_on = None

def upgrade():
    # Column already exists due to partial migration earlier
    # We skip re-adding to avoid duplicate column error
    pass

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('company_id')

    # ### end Alembic commands ###

"""Add total_points to User

Revision ID: 135b6ebf34df
Revises: b2ba0b4dc5ef
Create Date: 2025-03-29 20:11:45.670627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135b6ebf34df'
down_revision = 'b2ba0b4dc5ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.alter_column('company_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key('fk_review_company_id', 'company', ['company_id'], ['id'])


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('company_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###

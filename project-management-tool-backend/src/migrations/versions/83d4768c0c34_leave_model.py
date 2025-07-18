"""leave model

Revision ID: 83d4768c0c34
Revises: 7c3ebd4eb434
Create Date: 2025-06-03 17:15:50.679392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83d4768c0c34'
down_revision = '7c3ebd4eb434'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leave',
    sa.Column('leave_id', sa.String(length=22), nullable=False),
    sa.Column('employee_id', sa.String(), nullable=False),
    sa.Column('leave_type', sa.String(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('is_half_day', sa.Boolean(), nullable=True),
    sa.Column('reason', sa.String(length=225), nullable=True),
    sa.Column('applied_on', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], ),
    sa.PrimaryKeyConstraint('leave_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leave')
    # ### end Alembic commands ###

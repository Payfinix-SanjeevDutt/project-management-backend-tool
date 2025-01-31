"""comments

Revision ID: 6afc5e6dfe4b
Revises: 2f6cd6cf5888
Create Date: 2024-12-23 16:21:16.494315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6afc5e6dfe4b'
down_revision = '2f6cd6cf5888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('comment_id', sa.String(length=22), nullable=False),
    sa.Column('employee_id', sa.String(), nullable=True),
    sa.Column('task_id', sa.String(length=22), nullable=True),
    sa.Column('employee_name', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('action', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.task_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###

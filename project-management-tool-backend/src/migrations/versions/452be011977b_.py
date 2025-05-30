"""empty message

Revision ID: 452be011977b
Revises: cf0026ae2b7d
Create Date: 2024-11-07 15:10:19.132508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '452be011977b'
down_revision = 'cf0026ae2b7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sprints',
    sa.Column('sprint_id', sa.String(length=22), nullable=False),
    sa.Column('project_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('actual_start_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('actual_end_date', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('sprint_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sprints')
    # ### end Alembic commands ###

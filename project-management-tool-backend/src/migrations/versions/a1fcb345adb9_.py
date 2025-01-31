"""empty message

Revision ID: a1fcb345adb9
Revises: 526dbe1a4003
Create Date: 2024-12-11 10:48:37.162518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1fcb345adb9'
down_revision = '526dbe1a4003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('stage_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.create_foreign_key(None, 'sprints', ['sprint_id'], ['sprint_id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('stage_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###

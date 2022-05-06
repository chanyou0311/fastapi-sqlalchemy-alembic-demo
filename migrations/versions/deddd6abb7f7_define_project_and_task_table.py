"""Define project and task table

Revision ID: deddd6abb7f7
Revises: 
Create Date: 2022-05-05 15:25:04.779688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deddd6abb7f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('is_completed', sa.Boolean(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('projects')
    # ### end Alembic commands ###
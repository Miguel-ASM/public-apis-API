"""Create commits table

Revision ID: 4129f6834dcd
Revises: 10b49dfa4e22
Create Date: 2023-11-06 19:21:18.462411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4129f6834dcd'
down_revision = '10b49dfa4e22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apis_repo_commits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sha', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apis_repo_commits')
    # ### end Alembic commands ###

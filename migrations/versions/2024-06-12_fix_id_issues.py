"""fix id issues

Revision ID: 5cf0e65624b6
Revises: 7c5f710edb86
Create Date: 2024-06-12 13:38:09.284196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cf0e65624b6'
down_revision = '7c5f710edb86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crossection', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('dyke', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dyke', 'id')
    op.drop_column('crossection', 'id')
    # ### end Alembic commands ###

"""adding sensor dependency in readings corrected

Revision ID: f2c91833c6e6
Revises: 768c5bef0f68
Create Date: 2024-07-31 15:09:02.574221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2c91833c6e6'
down_revision: Union[str, None] = '768c5bef0f68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reading', 'sensor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reading', 'sensor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
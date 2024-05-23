"""create tables

Revision ID: c05a23491d31
Revises: 
Create Date: 2024-05-23 22:07:35.816037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c05a23491d31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('car_model', sa.String(), nullable=False),
    sa.Column('car_color', sa.String(), nullable=False),
    sa.Column('car_number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_from', sa.String(), nullable=False),
    sa.Column('address_to', sa.String(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(), nullable=True),
    sa.Column('id_user', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'CANCEL', name='status'), nullable=False),
    sa.Column('id_order_message', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('order')
    op.drop_table('driver')
    # ### end Alembic commands ###

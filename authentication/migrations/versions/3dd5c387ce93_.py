"""empty message

Revision ID: 3dd5c387ce93
Revises: 41a73553fef1
Create Date: 2024-04-18 01:29:58.247925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dd5c387ce93'
down_revision: Union[str, None] = '41a73553fef1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'hashed_token',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=1000),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'hashed_token',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=300),
               existing_nullable=False)
    # ### end Alembic commands ###

"""add content coloumn to post table

Revision ID: 55e92b5c0263
Revises: c33be46fa9b9
Create Date: 2024-12-06 15:27:26.867240

"""
import sqlalchemy.sql.expression
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55e92b5c0263'
down_revision: Union[str, None] = 'c33be46fa9b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')

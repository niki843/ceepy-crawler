"""Create Screenshots table

Revision ID: 07e82457bcd4
Revises: 
Create Date: 2025-03-29 18:57:41.919569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07e82457bcd4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'screenshot',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('url', sa.String(512), nullable=False),
        sa.Column('path', sa.String(512), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('account')

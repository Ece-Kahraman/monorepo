"""add app operation

Revision ID: 60e213d02c2f
Revises: bf9d3d0bb324
Create Date: 2025-02-02 18:36:20.782752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60e213d02c2f'
down_revision: Union[str, None] = 'bf9d3d0bb324'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE ledger_operation ADD VALUE 'CONTENT_CREATION'")


def downgrade() -> None:
    pass

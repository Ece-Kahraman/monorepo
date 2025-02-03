"""add app operation

Revision ID: e3232e811244
Revises: acebd6a4d6d4
Create Date: 2025-02-03 00:33:51.303180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3232e811244'
down_revision: Union[str, None] = 'acebd6a4d6d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE ledgeroperation ADD VALUE 'CONTENT_CREATION'")


def downgrade() -> None:
    pass

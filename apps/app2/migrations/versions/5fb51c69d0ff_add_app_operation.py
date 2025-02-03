"""add app operation

Revision ID: 5fb51c69d0ff
Revises: 5226c36c35c9
Create Date: 2025-02-03 00:38:41.024770

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5fb51c69d0ff"
down_revision: Union[str, None] = "5226c36c35c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE ledgeroperation ADD VALUE 'CONTENT_ACCESS'")


def downgrade() -> None:
    pass

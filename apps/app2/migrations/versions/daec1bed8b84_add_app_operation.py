"""add app operation

Revision ID: daec1bed8b84
Revises: 380875523835
Create Date: 2025-02-02 18:53:35.671918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daec1bed8b84'
down_revision: Union[str, None] = '380875523835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE ledger_operation ADD VALUE 'CONTENT_ACCESS'")


def downgrade() -> None:
    pass

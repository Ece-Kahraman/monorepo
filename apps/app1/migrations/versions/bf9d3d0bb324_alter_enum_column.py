"""alter enum column

Revision ID: bf9d3d0bb324
Revises: 06cad193b607
Create Date: 2025-02-02 18:34:34.175579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf9d3d0bb324'
down_revision: Union[str, None] = '06cad193b607'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM type if not exists
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ledger_operation') THEN
                CREATE TYPE ledger_operation AS ENUM (
                    'DAILY_REWARD',
                    'SIGNUP_CREDIT',
                    'CREDIT_SPEND',
                    'CREDIT_ADD'
                );
            END IF;
        END $$;
    """)
    
    # Create/update the `operation` column to use the ENUM
    op.alter_column(
        'ledger_entries',
        'operation',
        type_=sa.Enum(
            'DAILY_REWARD', 'SIGNUP_CREDIT', 'CREDIT_SPEND', 'CREDIT_ADD',
            name='ledger_operation'
        ),
        postgresql_using='operation::ledger_operation'
    )


def downgrade() -> None:
    pass

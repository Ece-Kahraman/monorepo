"""alter enum column

Revision ID: 5226c36c35c9
Revises: ba5ec5c9e004
Create Date: 2025-02-03 00:37:58.412581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5226c36c35c9'
down_revision: Union[str, None] = 'ba5ec5c9e004'
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
            name='ledgeroperation'
        ),
        postgresql_using='operation::ledgeroperation'
    )


def downgrade() -> None:
    pass

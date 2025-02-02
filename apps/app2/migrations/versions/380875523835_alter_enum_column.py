"""alter enum column

Revision ID: 380875523835
Revises: 1ca3197351b2
Create Date: 2025-02-02 18:52:41.161722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '380875523835'
down_revision: Union[str, None] = '1ca3197351b2'
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

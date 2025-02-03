"""alter enum column

Revision ID: acebd6a4d6d4
Revises: d12df45acfb9
Create Date: 2025-02-03 00:31:44.627509

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "acebd6a4d6d4"
down_revision: Union[str, None] = "d12df45acfb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM type if not exists
    op.execute(
        """
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
    """
    )

    # Create/update the `operation` column to use the ENUM
    op.alter_column(
        "ledger_entries",
        "operation",
        type_=sa.Enum(
            "DAILY_REWARD",
            "SIGNUP_CREDIT",
            "CREDIT_SPEND",
            "CREDIT_ADD",
            name="ledgeroperation",
        ),
        postgresql_using="operation::ledgeroperation",
    )


def downgrade() -> None:
    pass

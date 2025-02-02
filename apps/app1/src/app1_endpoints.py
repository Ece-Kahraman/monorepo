from core.ledgers.endpoint_logics import reach_endpoints
from apps.app1.src.app1_config import APP1_LEDGER_CONFIG
from apps.app1.src.app1_schemas import App1LedgerOperation

ledger_router = reach_endpoints(
    app_enum=App1LedgerOperation,
    app_config=APP1_LEDGER_CONFIG
)
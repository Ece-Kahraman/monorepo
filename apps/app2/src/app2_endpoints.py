from core.ledgers.endpoint_logics import reach_endpoints
from apps.app2.src.app2_config import APP2_LEDGER_CONFIG
from apps.app2.src.app2_schemas import App2LedgerOperation


ledger_router = reach_endpoints(
    app_enum=App2LedgerOperation,
    app_config=APP2_LEDGER_CONFIG
)
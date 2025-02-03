from core.ledgers.endpoint_logics import reach_endpoints
from apps.app2.src.app2_config import APP2_LEDGER_CONFIG

"""App Router is configured with APP2_LEDGER_CONFIG"""
ledger_router = reach_endpoints(
    app_config=APP2_LEDGER_CONFIG
)
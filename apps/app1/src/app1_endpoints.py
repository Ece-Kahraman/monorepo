from core.ledgers.endpoint_logics import reach_endpoints
from apps.app1.src.app1_config import APP1_LEDGER_CONFIG

"""App Router is configured with APP1_LEDGER_CONFIG"""
ledger_router = reach_endpoints(
    app_config=APP1_LEDGER_CONFIG
)
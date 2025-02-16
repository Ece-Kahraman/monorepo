from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.ledgers.services import LedgerService
from core.ledgers.schemas import LedgerEntrySchema


"""
Sets a central endpoint logic for the apps.
This way, it is easier to add or remove apps.
Arg:
    app_config: app specific operations configuration
Returns:
    APIRouter
"""


def reach_endpoints(app_config: dict[str, int]) -> APIRouter:

    ep = APIRouter()
    ledger_logic = LedgerService()

    """
    Get current balance for a user
    """

    @ep.get("/ledger/{owner_id}")
    def get_owner_balance(
        owner_id: str, db_session: Annotated[Session, Depends(get_db)]
    ):
        return {"balance": ledger_logic.get_balance(db_session, owner_id)}

    """
    Create a new ledger entry
    """

    @ep.post("/ledger")
    def post_new_ledger(
        new_ledger: LedgerEntrySchema, db_session: Annotated[Session, Depends(get_db)]
    ):
        new_entry = ledger_logic.post_ledger(
            db_session,
            new_ledger.operation.value,
            new_ledger.amount,
            new_ledger.nonce,
            new_ledger.owner_id,
            app_config,
        )
        return {"id": new_entry.id}

    return ep

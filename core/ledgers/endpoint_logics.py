from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.ledgers.services import LedgerService
from core.ledgers.schemas import LedgerEntrySchema, LedgerOperationType


def reach_endpoints(app_enum: type[LedgerOperationType], app_config: dict[str, int]) -> APIRouter:

    ep = APIRouter()
    ledger_logic = LedgerService()

    @ep.get("/ledger/{owner_id}")
    def get_owner_balance(
        owner_id: str, db_session: Annotated[Session, Depends[get_db]]
    ):
        return {"balance": ledger_logic.get_balance(db_session, owner_id)}

    @ep.post("/ledger")
    def post_new_ledger(
        new_ledger: LedgerEntrySchema[LedgerOperationType], db_session: Annotated[Session, Depends[get_db]]
    ):
        new_entry_id = ledger_logic.post_ledger(
            db_session,
            new_ledger.operation.value,
            new_ledger.nonce,
            new_ledger.owner_id,
            app_config,
        )
        return {"new ledger id": new_entry_id}

    return ep

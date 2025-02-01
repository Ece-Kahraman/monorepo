from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.ledgers.services import LedgerService


def reach_endpoints() -> APIRouter:  # take app specific parameters like its config dict

    ep = APIRouter()
    ledger_logic = LedgerService()

    @ep.get("/ledger/{owner_id}")
    def get_owner_balance(owner_id: str, session: Annotated[Session, Depends[get_db]]):
        return {"balance": ledger_logic.get_balance(session, owner_id)}
    
    return ep
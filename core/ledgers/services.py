from core.ledgers.models import LedgerEntryModel
from sqlalchemy.orm import Session


class LedgerService:

    def get_balance(self, db: Session, owner_id: str) -> int:
        entries = db.query(LedgerEntryModel).filter(LedgerEntryModel.owner_id == owner_id).all()
        balance = sum(entry.amount for entry in entries)
        return int(balance)
    
    def post_ledger(self):
        pass

    def _check_duplicate(self, db: Session, owner_id: str, nonce: str) -> bool:
        return db.query(LedgerEntryModel.id).filter(LedgerEntryModel.owner_id == owner_id, LedgerEntryModel.nonce == nonce).first() is not None

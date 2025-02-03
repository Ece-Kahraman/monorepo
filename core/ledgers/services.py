from datetime import datetime, timezone
from core.ledgers.models import LedgerEntryModel
from sqlalchemy.orm import Session


class LedgerService:

    def get_balance(self, db: Session, owner_id: str) -> int:
        entries = (
            db.query(LedgerEntryModel)
            .filter(LedgerEntryModel.owner_id == owner_id)
            .all()
        )
        balance = sum(entry.amount for entry in entries)
        return int(balance)

    def post_ledger(
        self,
        db: Session,
        operation: str,
        nonce: str,
        owner_id: str,
        app_config: dict[str, int],
    ) -> LedgerEntryModel:
        # checks
        if operation not in app_config:
            raise ValueError("Invalid operation: " + operation)

        if self._check_duplicate(db, owner_id, nonce):
            raise ValueError("Duplicate transaction")

        if app_config[operation] < 0 and self.get_balance(db, owner_id) < abs(app_config[operation]):
            raise ValueError("Insufficient balance")

        # create and post
        new_entry = LedgerEntryModel(
            operation=operation,
            amount=app_config[operation],
            nonce=nonce,
            owner_id=owner_id,
            created_on=datetime.now(timezone.utc)
        )
        db.add(new_entry)
        db.commit()
        return new_entry

    def _check_duplicate(self, db: Session, owner_id: str, nonce: str) -> bool:
        return (
            db.query(LedgerEntryModel.id)
            .where(
                LedgerEntryModel.owner_id == owner_id, LedgerEntryModel.nonce == nonce
            )
            .first()
            is not None
        )

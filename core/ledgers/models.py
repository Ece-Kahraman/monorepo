from sqlalchemy import Column, Integer, String, DateTime, Enum
from core.database import Base
from core.ledgers.schemas import LedgerOperation


class LedgerEntryModel(Base):
    __tablename__ = "ledger_entries"
    id = Column(Integer, primary_key=True)
    operation = Column(type_=Enum(LedgerOperation), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)

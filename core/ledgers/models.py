from sqlalchemy import Column, Integer, String, DateTime, Enum
from core.database import Base
from core.ledgers.models import LedgerOperation
from sqlalchemy.dialects.postgresql import ENUM


class LedgerEntryModel(Base):
    __tablename__ = "ledger_entries"
    id = Column(Integer, primary_key=True)
    operation = Column(Enum(LedgerOperation), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)

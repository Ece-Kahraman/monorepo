from sqlalchemy import Column, Integer, String, DateTime, Enum
from core.database import Base
from core.ledgers.schemas import LedgerOperation


"""Database model representing a ledger entry"""
class LedgerEntryModel(Base):
    __tablename__ = "ledger_entries"
    id = Column(Integer, primary_key=True) # Primary key
    operation = Column(type_=Enum(LedgerOperation), nullable=False) # Enum-constrained operation type
    amount = Column(Integer, nullable=False) # Operation credit amount
    nonce = Column(String, nullable=False) # Unique transaction ID
    owner_id = Column(String, nullable=False) # User identifier
    created_on = Column(DateTime, nullable=False) # Automatic timestamping

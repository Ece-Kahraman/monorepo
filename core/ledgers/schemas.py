from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class LedgerEntrySchema(BaseModel):
    operation: Enum
    amount: int
    nonce: str
    owner_id: str
    created_on: datetime

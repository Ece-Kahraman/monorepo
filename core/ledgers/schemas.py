from enum import Enum, EnumMeta
from pydantic import BaseModel, Field
from datetime import datetime

class RequiredOperationsMeta(EnumMeta):
    def __new__(cls, name, bases, app_operations):
        required = {"DAILY_REWARD", "SIGNUP_CREDIT", "CREDIT_SPEND", "CREDIT_ADD"}
        for op in required:
            if op not in app_operations:
                raise TypeError(f"{name} must include {op}")
        return super().__new__(cls, name, bases, app_operations)
    
class LedgerOperation(str, Enum):
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

class LedgerEntrySchema(BaseModel):
    operation: LedgerOperation
    amount: int
    nonce: str
    owner_id: str
    created_on: datetime = Field(default_factory=datetime.utcnow)

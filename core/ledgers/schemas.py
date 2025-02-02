from enum import Enum, EnumMeta
from pydantic import BaseModel
from datetime import datetime

class RequiredOperationsMeta(EnumMeta):
    def __new__(cls, name, bases, app_operations):
        required = {"DAILY_REWARD", "SIGNUP_CREDIT", "CREDIT_SPEND", "CREDIT_ADD"}
        for op in required:
            if op not in app_operations:
                raise TypeError(f"{name} must include {op}")
        return super().__new__(cls, name, bases, app_operations)

class LedgerEntrySchema(BaseModel):
    operation: Enum
    amount: int
    nonce: str
    owner_id: str
    created_on: datetime

from enum import Enum
from core.ledgers.schemas import RequiredOperationsMeta


"""App Specific Ledger Enumeration"""
class App2LedgerOperation(str, Enum, metaclass=RequiredOperationsMeta):
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
    CONTENT_ACCESS = "CONTENT_ACCESS"

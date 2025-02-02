from enum import Enum

class App1LedgerOperation(str, Enum):
    # Core operations (required)
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
    
    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"

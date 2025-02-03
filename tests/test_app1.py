import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# Force the core folder to be reachable
import sys
from pathlib import Path
monorepo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(monorepo_root))

from core.database import Base, get_db, _URL
from core.ledgers.services import LedgerService
from core.ledgers.schemas import LedgerOperation
from apps.app1.app1_main import app
from apps.app1.src.app1_config import APP1_LEDGER_CONFIG


engine = create_engine(_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixtures
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def ledger_service(db_session):
    return LedgerService()

# Test data
TEST_USER = "user_123"
TEST_NONCE = "nonce_abc"
TEST_OPERATIONS = [
    (LedgerOperation.DAILY_REWARD, APP1_LEDGER_CONFIG["DAILY_REWARD"]),
    (LedgerOperation.SIGNUP_CREDIT, APP1_LEDGER_CONFIG["SIGNUP_CREDIT"]),
]

# Tests

"""
Tests if the app creates a valid ledger entry.
Args:
    client: Test client with overridden database dependency
    ledger_service: Function to reach the LedgerService
    db_session: Database session with transaction rollback after each test
Returns:
    Success if the test entry is created
"""
def test_create_valid_entry(client, ledger_service, db_session):
    payload = {
        "operation": LedgerOperation.DAILY_REWARD.value,
        "amount": APP1_LEDGER_CONFIG["DAILY_REWARD"],
        "nonce": TEST_NONCE,
        "owner_id": TEST_USER,
        "created_on": datetime.now(timezone.utc).isoformat()
    }
    
    response = client.post("/app1/ledger", json=payload)
    print(response.json())
    assert response.status_code == 200
    assert "id" in response.json()
    
    balance = ledger_service.get_balance(db_session, TEST_USER)
    assert balance == APP1_LEDGER_CONFIG["DAILY_REWARD"]

"""
Tests if user balance is still retrieved with 0.
Args:
    client: Test client with overridden database dependency
Returns:
    Success if balance is calculated as 0
"""
def test_get_balance_empty(client):
    response = client.get(f"/app1/ledger/{TEST_USER}")
    assert response.status_code == 200
    assert response.json() == {"balance": 0}


"""
Tests if the business logic catches a duplicate nonce
Args:
    client: Test client with overridden database dependency
Returns:
    Success if the logic raises the correct error
"""
def test_duplicate_nonce_rejection(client):
    payload = {
        "operation": LedgerOperation.SIGNUP_CREDIT.value,
        "amount": APP1_LEDGER_CONFIG["SIGNUP_CREDIT"],
        "nonce": TEST_NONCE,
        "owner_id": TEST_USER
    }
    
    response1 = client.post("/app1/ledger", json=payload)
    assert response1.status_code == 200
    
    # this one intentionally fails
    response2 = client.post("/app1/ledger", json=payload)
    assert response2.status_code == 400
    assert "Duplicate transaction" in response2.text


"""
Tests if the business logic catches an insufficient balance
Args:
    client: Test client with overridden database dependency
Returns:
    Success if the logic raises the correct error
"""
def test_insufficient_balance(client):
    # this test intentionally fails to test the entry balance conditions
    # create initial debit that would put balance negative
    payload = {
        "operation": LedgerOperation.CREDIT_SPEND.value,
        "amount": APP1_LEDGER_CONFIG["CREDIT_SPEND"],
        "nonce": TEST_NONCE,
       "owner_id": TEST_USER
    }
    
    response = client.post("/app1/ledger", json=payload)
    assert response.status_code == 400
    assert "Insufficient balance" in response.text


"""
Tests if the business logic catches an invalid operation
Args:
    client: Test client with overridden database dependency
Returns:
    Success if the logic raises the correct error
"""
def test_invalid_operation(client):
    payload = {
        "operation": "CONTENT_ACCESS", # app2's own operation
        "amount": 10,
        "nonce": TEST_NONCE,
        "owner_id": TEST_USER
    }
    
    response = client.post("/app1/ledger", json=payload)
    assert response.status_code == 422  # passes the test because it is an invalid op


"""
Tests if the business logic catches a mismatch between the
amount and the operation, comparing to the relevent app_config
Args:
    client: Test client with overridden database dependency
Returns:
    Success if the logic raises the correct error
"""
def test_operation_amount_mismatch(client): # This test intentionally fails
    payload = {
        "operation": LedgerOperation.DAILY_REWARD.value,
        "amount": 100,  # Should be 1 according to config
        "nonce": TEST_NONCE,
        "owner_id": TEST_USER
    }
    
    response = client.post("/app1/ledger", json=payload)
    assert response.status_code == 400
    assert "Amount mismatch" in response.text


"""
Compares the expected balance and the calculated balance
Args:
    client: Test client with overridden database dependency
    ledger_service: Function to reach the LedgerService
Returns:
    Success if the the balances are the same
"""
def test_balance_calculation(client, ledger_service):
    # Test cumulative balance
    for i, (operation, amount) in enumerate(TEST_OPERATIONS):
        payload = {
            "operation": operation.value,
            "amount": amount,
            "nonce": f"{TEST_NONCE}_{i}",
            "owner_id": TEST_USER
        }
        response = client.post("/app1/ledger", json=payload)
        assert response.status_code == 200
    
    expected_balance = sum(amount for _, amount in TEST_OPERATIONS)
    response = client.get(f"/app1/ledger/{TEST_USER}")
    assert response.json()["balance"] == expected_balance


"""
Compares the expected balance of a group of mixed operations
and their calculated balance
Args:
    client: Test client with overridden database dependency
    ledger_service: Function to reach the LedgerService
Returns:
    Success if the the balances are the same
"""
def test_mixed_operations(client, ledger_service):
    # Test credit and debit operations
    credits = [
        (LedgerOperation.DAILY_REWARD, 1),
        (LedgerOperation.CREDIT_ADD, 10)
    ]
    
    debits = [
        (LedgerOperation.CREDIT_SPEND, -1)
    ]
    
    # Add all operations
    for i, (operation, amount) in enumerate(credits + debits):
        payload = {
            "operation": operation.value,
            "amount": amount,
            "nonce": f"{TEST_NONCE}_{i}",
            "owner_id": TEST_USER
        }
        response = client.post("/app1/ledger", json=payload)
        assert response.status_code == 200
    
    expected_balance = sum(amount for _, amount in credits + debits)
    response = client.get(f"/app1/ledger/{TEST_USER}")
    assert response.json()["balance"] == expected_balance
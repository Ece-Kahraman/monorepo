from fastapi import FastAPI
from apps.app1.src.app1_endpoints import ledger_router


app = FastAPI(title="App1 Ledger API")

app.include_router(ledger_router, prefix="/app1")


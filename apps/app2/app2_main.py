from fastapi import FastAPI
from apps.app2.src.app2_endpoints import ledger_router


app = FastAPI()

app.include_router(ledger_router, prefix="/app2")


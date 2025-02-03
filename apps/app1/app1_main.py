from fastapi import FastAPI
from apps.app1.src.app1_endpoints import ledger_router


app = FastAPI()

"""App1 mounts onto the shared endpoint logics"""
app.include_router(ledger_router, prefix="/app1")

from fastapi import FastAPI

from src.app.api.auth_router import router as auth_router
from src.app.api.healthz.healthz_router import router as healthz_router
from src.app.api.transaction_router import router as transaction_router
from src.app.api.verify_router import router as verify_router

app = FastAPI(prefix="/api")
app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(verify_router)
app.include_router(healthz_router)

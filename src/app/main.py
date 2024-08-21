from fastapi import FastAPI

from src.app.api.auth_router import router as auth_router
from src.app.api.registrate_router import router as registrate_router
from src.app.api.report_router import router as report_router
from src.app.api.transaction_router import router as transaction_router
from src.app.api.verify_router import router as verify_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(registrate_router)
app.include_router(transaction_router)
app.include_router(report_router)
app.include_router(verify_router)

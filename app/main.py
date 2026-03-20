from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.db.init_db import init_db

setup_logging()

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router, prefix = "/api/v1")

@app.get("/")
def health_check():
    return {"message": "Okay"}

@app.on_event("startup")
def on_startup():
    init_db()

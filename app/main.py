from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.db.init_db import init_db

setup_logging()

app = FastAPI(title=settings.APP_NAME)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "ok"}

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@app.on_event("startup")
def on_startup():
    init_db()

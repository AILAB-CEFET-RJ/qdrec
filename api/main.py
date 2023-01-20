from dataclasses import dataclass
from datetime import datetime

from fastapi import FastAPI

from querido_diario.db.engine import init_db
from querido_diario.routers import excerpts

app = FastAPI()

DB_FILE = "sqlite:///qd_prototipo.db"

@app.on_event("startup")
def startup_event():
    init_db(DB_FILE) 

@app.get("/")
def read_root():
    return "The server is running"

app.include_router(excerpts.router)
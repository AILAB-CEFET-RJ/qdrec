from dataclasses import dataclass

from fastapi import FastAPI

from querido_diario.db.engine import init_db
from querido_diario.routers import excerpts

from database.connection import SessionLocal, engine

app = FastAPI()

@app.get("/")
def read_root():
    return "The server is running"



app.include_router(excerpts.router)
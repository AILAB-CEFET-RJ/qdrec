from dataclasses import dataclass

from fastapi import FastAPI

from api.querido_diario.routers import excerpts

from database.connection import SessionLocal, engine

app = FastAPI()

app.include_router(excerpts.router)
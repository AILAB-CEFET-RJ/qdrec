from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from querido_diario.db.models import Base

engine: Engine = None
DBSession = sessionmaker()
def init_db(filepath: str):
    """Create database tables for our data models."""
    engine = create_engine(filepath)
    Base.metadata.bind = engine
    DBSession.bind = engine

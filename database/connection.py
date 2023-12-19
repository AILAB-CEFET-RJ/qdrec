from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

# conexão com senha normal
engine = create_engine("postgresql://user:password@localhost/NomedoDatabase")

# conexão com senha com caracteres especiais
# engine = create_engine("postgresql://user:%s@localhost/NomedoDatabase" % quote('password'))

engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
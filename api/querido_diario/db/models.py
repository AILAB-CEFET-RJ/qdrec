from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.types import PickleType

Base = declarative_base()

class DBExcerpts(Base):
    __tablename__ = 'excerpts'

    excerpt_id = Column(String(100), 
                     primary_key=True,
                     nullable=False, 
                     unique=True)
    excerpt_processed = Column(String(10005),
                  nullable=False)
    city = Column(String(50), 
                  nullable=False)
    state = Column(String(2),
                   nullable=False)
    excerpt_vector = Column(String(10),#PickleType
                        nullable=False)
    source_date = Column(Date, 
                  nullable=False)

#    def __repr__(self):
#        return f"Excerpt: {self.excerpt_processed} - Date: {self.source_date} - City: {self.state} - State: {self.city} - Vector: {self.excerpt_vector}"


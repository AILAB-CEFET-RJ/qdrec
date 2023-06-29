from sqlalchemy import *
#from sqlalchemy_orm import Model, Database
from sqlalchemy.orm import relationship
from database.connection import Base
from sqlalchemy.dialects.postgresql import TSVECTOR

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

class ExcerptMetadata(Base):
    __tablename__ = 'excerpt_metadata'
    __table_args__ = {'extend_existing': True} 
    excerpt_id=Column(String(100), primary_key=True)
    uf=Column('uf', String(32))
    cidade=Column('cidade', String(32))
    tema=Column('tema', String(32))
    data=Column('data', String(32))
    named_entity = relationship("NamedEntity")

class NamedEntity(Base):
    __tablename__ = 'named_entity'
    __table_args__ = {'extend_existing': True} 
    excerpt_id = Column(String(100), ForeignKey('excerpt_metadata.excerpt_id'), primary_key=True)
    content=Column('content', TEXT, primary_key=True)
    entity_type=Column('entity_type', String(32))
    start_offset=Column('start_offset', Integer)
    end_offset=Column('end_offset', Integer)

class Vectors(Base):
    __tablename__ = 'vectors'
    __table_args__ = {'extend_existing': True}
    excerpt_id = Column(Integer, ForeignKey('excerpt_metadata.excerpt_id'))
    vectorized_excerpt = Column('vectorized_excerpt', TSVECTOR, primary_key=True)
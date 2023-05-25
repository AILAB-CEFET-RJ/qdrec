from sqlalchemy import *
from sqlalchemy_orm import Model, Database
from sqlalchemy.orm import relationship

Base = Model()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

class ExcerptMetadata(Base):
    __tablename__ = 'excerpt_metadata'
    excerpt_id=Column(Integer, primary_key=True)
    uf=Column('uf', String(32))
    cidade=Column('cidade', String(32))
    tema=Column('tema', String(32))
    data=Column('data', DateTime)
    named_entity = relationship("NamedEntity")

class NamedEntity(Base):
    __tablename__ = 'named_entity'
    # circumventing sqlalchemy limitation of not allowing tables without PK
    column_not_exist_in_db = Column(Integer, primary_key=True)
    excerpt_id = Column(Integer, ForeignKey('excerpt_metadata.excerpt_id'))
    content=Column('content', String(32))
    entity_type=Column('entity_type', String(32))
    start_offset=Column('start_offset', Integer)
    end_offset=Column('end_offset', Integer)

db = Database("sqlite:///:memory:")
db.create(NamedEntity)

test = NamedEntity(excerpt_id=123, content='JAIME CRUZ', entity_type='PERSON', start_offset=0, end_offset=10)

session = db.session()
session.create(test)

result = session.query(NamedEntity).filter(NamedEntity.excerpt_id == 123).one()
print(object_as_dict(result))

session.commit()
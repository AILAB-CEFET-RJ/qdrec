import datetime
from pydantic import BaseModel

##  EXCERPT METADATA  ##
class ExcerptMetadataBase(BaseModel):
    excerpt_id: str
    uf: str
    cidade: str
    tema: str
    data: datetime.datetime

class ExcerptMetadataCreate(ExcerptMetadataBase):
    pass

class ExcerptMetadata(ExcerptMetadataBase):
    excerpt_id: str
    tema: str

    class Config:
        orm_mode = True

##  NAMED ENTITY  ##
class NamedEntityBase(BaseModel):
    excerpt_id: str
    content: str
    entity_type: str
    start_offset: int
    end_offset: int

class NamedEntityCreate(NamedEntityBase):
    pass

class NamedEntity(NamedEntityBase):
    excerpt_id: str
    entity_type: str

    class Config:
        orm_mode = True

##  VECTORS  ##
class VectorsBase(BaseModel):
    excerpt_id: str
    vectorized_excerpt: str

class VectorsCreate(VectorsBase):
    pass

class Vectors(VectorsBase):
    excerpt_id: str

    class Config:
        orm_mode = True
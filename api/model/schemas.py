from pydantic import BaseModel
from datetime import date

##  EXCERPT METADATA  ##
class ExcerptMetadataBase(BaseModel):
    excerpt_id: int
    uf: str
    cidade: str
    tema: str
    data: date

class ExcerptMetadataCreate(ExcerptMetadataBase):
    pass

class ExcerptMetadata(ExcerptMetadataBase):
    excerpt_id: int
    tema: str

    class Config:
        orm_mode = True

##  NAMED ENTITY  ##
class NamedEntityBase(BaseModel):
    excerpt_id: int
    content: str
    entity_type: str
    start_offset: int
    end_offset: int

class NamedEntityCreate(NamedEntityBase):
    pass

class NamedEntity(NamedEntityBase):
    excerpt_id: int
    entity_type: str

    class Config:
        orm_mode = True

##  VECTORS  ##
class VectorsBase(BaseModel):
    excerpt_id: int
    vectorized_excerpt: str

class VectorsCreate(VectorsBase):
    pass

class Vectors(VectorsBase):
    excerpt_id: int

    class Config:
        orm_mode = True
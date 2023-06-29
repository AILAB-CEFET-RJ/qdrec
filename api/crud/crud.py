from sqlalchemy.orm import Session

from api.model import excerpt_models, schemas

def get_excerpt_metadata_by_id(db: Session, excerpt_id: str):
    return db.query(excerpt_models.ExcerptMetadata).filter(excerpt_models.ExcerptMetadata.excerpt_id == excerpt_id).first()

def get_excerpt_metadata(db: Session, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.ExcerptMetadata).offset(skip).limit(limit).all()

def get_named_entities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.NamedEntity).offset(skip).limit(limit).all()

def get_named_entities_by_excerpt_id(db: Session, excerpt_id: str, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.NamedEntity).filter(excerpt_models.NamedEntity.excerpt_id == excerpt_id).offset(skip).limit(limit).all()

def get_vectors_by_excerpt_id(db: Session, excerpt_id: str, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.Vectors).filter(excerpt_models.Vectors.excerpt_id == excerpt_id).offset(skip).limit(limit).all()

def create_excerpt_metadata(db: Session, excerpt_metadata: schemas.ExcerptMetadataCreate):
    db_excerpt_metadata = get_excerpt_metadata_by_id(db, excerpt_id=excerpt_metadata.excerpt_id)
    if not db_excerpt_metadata:
        db_excerpt_metadata = excerpt_models.ExcerptMetadata(
            excerpt_id=excerpt_metadata.excerpt_id,
            uf=excerpt_metadata.uf,
            cidade=excerpt_metadata.cidade,
            tema=excerpt_metadata.tema,
            data=excerpt_metadata.data
        )
        db.add(db_excerpt_metadata)
        db.commit()
        db.refresh(db_excerpt_metadata)
        return db_excerpt_metadata
    return

def create_named_entity(db: Session, named_entity: schemas.NamedEntityCreate):
    db_excerpt_metadata = get_unique_named_entity(db, named_entity)
    if not db_excerpt_metadata:
        db_named_entity = excerpt_models.NamedEntity(
            excerpt_id=named_entity.excerpt_id,
            content=named_entity.content,
            entity_type=named_entity.entity_type,
            start_offset=named_entity.start_offset,
            end_offset=named_entity.end_offset
        )
        db.add(db_named_entity)
        db.commit()
        db.refresh(db_named_entity)
        return db_named_entity
    return

def get_unique_named_entity(db: Session, named_entity: schemas.NamedEntity):
    return db.query(excerpt_models.NamedEntity).filter(excerpt_models.NamedEntity.content == named_entity.content).filter(excerpt_models.NamedEntity.excerpt_id == named_entity.excerpt_id).filter(excerpt_models.NamedEntity.start_offset == named_entity.start_offset).first()
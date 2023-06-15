from sqlalchemy.orm import Session

from api.model import excerpt_models

def get_excerpt_metadata_by_id(db: Session, excerpt_id: int):
    return db.query(excerpt_models.ExcerptMetadata).filter(excerpt_models.ExcerptMetadata.excerpt_id == excerpt_id).first()

def get_named_entities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.NamedEntity).offset(skip).limit(limit).all()

def get_named_entities_by_excerpt_id(db: Session, excerpt_id: int, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.NamedEntity).filter(excerpt_models.NamedEntity.excerpt_id == excerpt_id).offset(skip).limit(limit).all()

def get_vectors_by_excerpt_id(db: Session, excerpt_id: int, skip: int = 0, limit: int = 100):
    return db.query(excerpt_models.Vectors).filter(excerpt_models.Vectors.excerpt_id == excerpt_id).offset(skip).limit(limit).all()
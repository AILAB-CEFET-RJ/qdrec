from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.model import schemas

from database.connection import SessionLocal

from api.crud import crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/health", status_code=200)
def health_check():
    return "The server is running"


@router.get("/excerpts/{excerpt_id}", response_model=schemas.ExcerptMetadata)
def read_excerpt_metadata(excerpt_id: int, db: Session = Depends(get_db)):
    db_excerpt_metadata = crud.get_excerpt_metadata_by_id(db, excerpt_id=excerpt_id)
    if db_excerpt_metadata is None:
        raise HTTPException(status_code=404, detail="Excerpt metadata not found")
    return db_excerpt_metadata

@router.get("/entities/", response_model=list[schemas.NamedEntity])
def read_named_entities(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_named_entities = crud.get_named_entities(db, skip, limit)
    return db_named_entities

@router.get("/entities/{excerpt_id}", response_model=list[schemas.NamedEntity])
def read_named_entities(excerpt_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_named_entities = crud.get_named_entities_by_excerpt_id(db, excerpt_id, skip, limit)
    return db_named_entities

@router.get("/vectors/{excerpt_id}", response_model=list[schemas.Vectors])
def read_named_entities(excerpt_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_vectors = crud.get_vectors_by_excerpt_id(db, excerpt_id, skip, limit)
    if not db_vectors:
        raise HTTPException(status_code=404, detail="Excerpt metadata not found")
    return db_vectors
    
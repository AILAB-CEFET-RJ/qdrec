from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from api.model import schemas

from database.connection import SessionLocal

from api.crud import crud
from scripts.bert_ner_processor import execute_csv
from scripts.append_regex import execute_csv_regex

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

####   EXCERPT_METADATA   ####

@router.get("/excerpt_metadata/{excerpt_id}", response_model=schemas.ExcerptMetadata)
def read_excerpt_metadata_by_id(excerpt_id: str, db: Session = Depends(get_db)):
    db_excerpt_metadata = crud.get_excerpt_metadata_by_id(db, excerpt_id=excerpt_id)
    if db_excerpt_metadata is None:
        raise HTTPException(status_code=404, detail="Excerpt metadata not found")
    return db_excerpt_metadata

@router.get("/excerpt_metadata/", response_model=list[schemas.ExcerptMetadata])
def read_excerpt_metadata(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_named_entities = crud.get_excerpt_metadata(db, skip, limit)
    return db_named_entities

@router.post("/excerpt_metadata/", response_model=schemas.ExcerptMetadata)
def create_excerpt_metadata(excerpt_metadata: schemas.ExcerptMetadataCreate, db: Session = Depends(get_db)):
    db_excerpt_metadata = crud.get_excerpt_metadata_by_id(db, excerpt_id=excerpt_metadata.excerpt_id)
    if db_excerpt_metadata:
        raise HTTPException(status_code=400, detail="Excerpt Metadata already registered")
    return crud.create_excerpt_metadata(db=db, excerpt_metadata=excerpt_metadata)

####   ENTITIES   ####

@router.get("/entities/", response_model=list[schemas.NamedEntity])
def read_named_entities(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_named_entities = crud.get_named_entities(db, skip, limit)
    return db_named_entities

@router.get("/entities/{excerpt_id}", response_model=list[schemas.NamedEntity])
def read_named_entities_by_id(excerpt_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_named_entity = crud.get_named_entities_by_excerpt_id(db, excerpt_id, skip, limit)
    return db_named_entity

@router.post("/entities/", response_model=schemas.NamedEntity)
def create_named_entity(named_entity: schemas.NamedEntityCreate, db: Session = Depends(get_db)):
    db_excerpt_metadata = crud.get_unique_named_entity(db, named_entity)
    if db_excerpt_metadata:
        raise HTTPException(status_code=400, detail="Named Entity already registered")
    return crud.create_named_entity(db=db, named_entity=named_entity)

####   VECTORS   ####

@router.get("/vectors/{excerpt_id}", response_model=list[schemas.Vectors])
def read_vectors(excerpt_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_vectors = crud.get_vectors_by_excerpt_id(db, excerpt_id, skip, limit)
    if not db_vectors:
        raise HTTPException(status_code=404, detail="Vector not found")
    return db_vectors

@router.post("/execute/")
def execute(file: UploadFile = File(...)):
    return execute_csv(file)

@router.post("/execute/regex")
def execute_regex(file: UploadFile = File(...)):
    return execute_csv_regex(file)
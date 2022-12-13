from fastapi import APIRouter, Depends, HTTPException, status
from querido_diario.operations.excerpts import ExcerptReadData, read_all_excerpts, read_excerpts

router = APIRouter()

@router.get("/excerpts")
def api_read_all_excerpts():
    """Read all excerpts from the database."""
    excerpts = read_all_excerpts()
    return excerpts


@router.post("/excerpts")
def api_read_excerpts(data: ExcerptReadData):
    print("routers")
    return read_excerpts(data)
    
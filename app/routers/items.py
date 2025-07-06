from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=schemas.ItemRead)
async def create(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, item)


@router.get("/{item_id}", response_model=schemas.ItemRead)
async def read(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/", response_model=list[schemas.ItemRead])
async def list_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.list_items(db, skip, limit)

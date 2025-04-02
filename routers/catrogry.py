from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.dbs import get_db
from models.base import Category, Document
from schemes.base import CategoryResponse, PaginationParams, DocumentResponse

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
        pagination: PaginationParams = Depends(),  # Pagination params as dependency
        db: AsyncSession = Depends(get_db)
):
    # Calculate offset based on page and per_page
    offset = (pagination.page - 1) * pagination.per_page

    # Query with pagination
    query = select(Category).offset(offset).limit(pagination.per_page)
    result = await db.execute(query)
    categories = result.scalars().all()

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return categories
@router.get("/{category_id}/documents/", response_model=List[DocumentResponse])
async def get_documents_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Document).where(Document.Category_ID == category_id)
    result = await db.execute(query)
    documents = result.scalars().all()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found for this category")
    return documents

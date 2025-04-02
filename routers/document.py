from datetime import datetime
from typing import Dict

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession

from configs.dbs import get_db
from models.base import Document, User, Modified_Document
from schemes.base import DocumentContentResponse, ModifiedDocumentCreate

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.get("/{document_id}/content/", response_model=DocumentContentResponse)
async def get_document_content(document_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Document).where(Document.Document_ID == document_id)
    result = await db.execute(query)
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"Document_ID": document.Document_ID, "Default_Content": document.Default_Content}


@router.post("/modified-documents/", response_model=str)
async def create_modified_document(
        modified_doc: ModifiedDocumentCreate,
        db: AsyncSession = Depends(get_db)
) -> str:
    try:
        # Verify User exists using async query
        user_result = await db.execute(
            select(User).where(User.User_ID == modified_doc.user_id)
        )
        user = user_result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User with ID {modified_doc.user_id} not found"
            )

        # Verify Document exists using async query
        doc_result = await db.execute(
            select(Document).where(Document.Document_ID == modified_doc.document_id)
        )
        document = doc_result.scalars().first()
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {modified_doc.document_id} not found"
            )
        # Create new Modified_Document instance
        db_modified_doc = Modified_Document(
            User_ID=modified_doc.user_id,
            Document_ID=modified_doc.document_id,
            Modified_Content=modified_doc.modified_content,
        )

        # Add to database
        db.add(db_modified_doc)
        await db.commit()
        await db.refresh(db_modified_doc)

        # Return response
        return "Modified document created successfully"
    except HTTPException as he:
        raise he
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred: {str(e)}"
        )

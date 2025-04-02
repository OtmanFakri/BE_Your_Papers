from typing import Optional

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    Category_ID: int
    Category_Name: str
    Description: str | None = None

    class Config:
        orm_mode = True


class DocumentResponse(BaseModel):
    Document_ID: int
    Title: str

    class Config:
        orm_mode = True


class DocumentContentResponse(BaseModel):
    Document_ID: int
    Default_Content: str

    class Config:
        orm_mode = True


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 100

class ModifiedDocumentCreate(BaseModel):
    user_id: int
    document_id: int
    modified_content: str
    payment_status: Optional[bool] = False
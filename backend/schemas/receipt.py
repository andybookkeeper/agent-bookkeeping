from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReceiptCreate(BaseModel):
    transaction_id: str
    file_path: str = Field(..., min_length=1, max_length=500)


class ReceiptUpdate(BaseModel):
    file_path: Optional[str] = Field(None, min_length=1, max_length=500)


class ReceiptResponse(BaseModel):
    id: str
    transaction_id: str
    file_path: str
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

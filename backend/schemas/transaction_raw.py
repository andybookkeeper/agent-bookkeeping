from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionRawCreate(BaseModel):
    date: datetime
    description: str = Field(..., min_length=1, max_length=500)
    amount: float = Field(..., gt=0)
    source: str = Field(..., min_length=1, max_length=100)


class TransactionRawUpdate(BaseModel):
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[float] = Field(None, gt=0)
    source: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[TransactionStatus] = None


class TransactionRawResponse(BaseModel):
    id: str
    date: datetime
    description: str
    amount: float
    source: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

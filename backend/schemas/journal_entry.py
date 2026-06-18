from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EntryType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class JournalEntryCreate(BaseModel):
    date: datetime
    description: str = Field(..., min_length=1, max_length=500)
    account_id: str
    amount: float = Field(..., gt=0)
    type: EntryType


class JournalEntryUpdate(BaseModel):
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[EntryType] = None


class JournalEntryResponse(BaseModel):
    id: str
    date: datetime
    description: str
    account_id: str
    amount: float
    type: EntryType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

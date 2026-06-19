from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EntryType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class JournalEntryCreate(BaseModel):
    date: datetime = Field(..., json_schema_extra={"deprecated": True})
    description: str = Field(..., min_length=1, max_length=500, json_schema_extra={"deprecated": True})
    account_id: str = Field(..., json_schema_extra={"deprecated": True})
    amount: float = Field(..., gt=0, json_schema_extra={"deprecated": True})
    type: EntryType = Field(..., json_schema_extra={"deprecated": True})


class JournalEntryPairCreate(BaseModel):
    date: datetime
    description: str = Field(..., min_length=1, max_length=500)
    debit_account_id: str
    credit_account_id: str
    amount: float = Field(..., gt=0)


class JournalEntryPairUpdate(BaseModel):
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[float] = Field(None, gt=0)


class JournalEntryUpdate(BaseModel):
    date: Optional[datetime] = Field(None, json_schema_extra={"deprecated": True})
    description: Optional[str] = Field(None, min_length=1, max_length=500, json_schema_extra={"deprecated": True})
    amount: Optional[float] = Field(None, gt=0, json_schema_extra={"deprecated": True})
    type: Optional[EntryType] = Field(None, json_schema_extra={"deprecated": True})


class JournalEntryResponse(BaseModel):
    id: str
    pair_id: Optional[str] = None
    date: datetime
    description: str
    account_id: str
    amount: float
    type: EntryType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

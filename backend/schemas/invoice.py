from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class InvoiceCreate(BaseModel):
    account_id: str
    amount: float = Field(..., gt=0)
    date: datetime
    due_date: datetime


class InvoiceUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: Optional[InvoiceStatus] = None


class InvoiceResponse(BaseModel):
    id: str
    account_id: str
    amount: float
    date: datetime
    due_date: datetime
    status: InvoiceStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

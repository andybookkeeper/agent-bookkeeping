from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    invoice_id: str
    amount: float = Field(..., gt=0)
    date: datetime
    method: str = Field(..., min_length=1, max_length=100)


class PaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None
    method: Optional[str] = Field(None, min_length=1, max_length=100)


class PaymentResponse(BaseModel):
    id: str
    invoice_id: str
    amount: float
    date: datetime
    method: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

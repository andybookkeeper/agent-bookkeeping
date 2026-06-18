from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AccountType(str, Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: AccountType
    balance: float = 0.0


class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    balance: Optional[float] = None


class AccountResponse(BaseModel):
    id: str
    name: str
    type: AccountType
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

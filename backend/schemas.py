from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Account Schemas
class AccountCreate(BaseModel):
    name: str
    type: str
    balance: float = 0.0


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    balance: Optional[float] = None


class AccountResponse(BaseModel):
    id: int
    name: str
    type: str
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# JournalEntry Schemas
class JournalEntryCreate(BaseModel):
    date: datetime
    description: str
    account_id: int
    amount: float
    type: str


class JournalEntryUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None


class JournalEntryResponse(BaseModel):
    id: int
    date: datetime
    description: str
    account_id: int
    amount: float
    type: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# TransactionRaw Schemas
class TransactionRawCreate(BaseModel):
    date: datetime
    description: str
    amount: float
    source: str


class TransactionRawUpdate(BaseModel):
    status: Optional[str] = None


class TransactionRawResponse(BaseModel):
    id: int
    date: datetime
    description: str
    amount: float
    source: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Invoice Schemas
class InvoiceCreate(BaseModel):
    account_id: int
    amount: float
    date: datetime
    due_date: datetime


class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None


class InvoiceResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    date: datetime
    due_date: datetime
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Payment Schemas
class PaymentCreate(BaseModel):
    invoice_id: int
    amount: float
    date: datetime
    method: str


class PaymentResponse(BaseModel):
    id: int
    invoice_id: int
    amount: float
    date: datetime
    method: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Receipt Schemas
class ReceiptCreate(BaseModel):
    transaction_id: int
    file_path: str


class ReceiptResponse(BaseModel):
    id: int
    transaction_id: int
    file_path: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

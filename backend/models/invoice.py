from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid

Base = declarative_base()


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Invoice(id={self.id}, amount={self.amount}, status={self.status})>"

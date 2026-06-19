from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from backend.models.base import Base
from sqlalchemy.orm import relationship
import enum
import uuid


class EntryType(str, enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pair_id = Column(String(36), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    description = Column(String(500), nullable=False)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(EntryType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<JournalEntry(id={self.id}, date={self.date}, amount={self.amount}, type={self.type})>"

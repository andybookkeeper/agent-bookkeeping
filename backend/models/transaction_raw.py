from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid

Base = declarative_base()


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionRaw(Base):
    __tablename__ = "transactions_raw"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime, nullable=False, index=True)
    description = Column(String(500), nullable=False)
    amount = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TransactionRaw(id={self.id}, date={self.date}, amount={self.amount}, status={self.status})>"

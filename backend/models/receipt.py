from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String, ForeignKey("transactions_raw.id"), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Receipt(id={self.id}, file_path={self.file_path})>"

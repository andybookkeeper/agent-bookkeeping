from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid

Base = declarative_base()


class AccountType(str, enum.Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    type = Column(Enum(AccountType), nullable=False)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Account(id={self.id}, name={self.name}, type={self.type}, balance={self.balance})>"

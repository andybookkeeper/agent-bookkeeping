from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.transaction_raw import TransactionRaw
from backend.schemas.transaction_raw import TransactionRawCreate, TransactionRawUpdate, TransactionRawResponse
from backend.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.get("/", response_model=List[TransactionRawResponse])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """List transactions with optional status filtering."""
    try:
        query = db.query(TransactionRaw)
        if status:
            query = query.filter(TransactionRaw.status == status)
        transactions = query.offset(skip).limit(limit).all()
        return transactions
    except SQLAlchemyError as e:
        logger.error(f"Database error listing transactions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch transactions")


@router.get("/{transaction_id}", response_model=TransactionRawResponse)
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """Get a specific transaction."""
    try:
        transaction = db.query(TransactionRaw).filter(TransactionRaw.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch transaction")


@router.post("/", response_model=TransactionRawResponse, status_code=201)
async def create_transaction(transaction: TransactionRawCreate, db: Session = Depends(get_db)):
    """Create a new transaction."""
    try:
        db_transaction = TransactionRaw(**transaction.dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        logger.info(f"Transaction created: {db_transaction.id}")
        return db_transaction
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create transaction")


@router.put("/{transaction_id}", response_model=TransactionRawResponse)
async def update_transaction(
    transaction_id: str,
    transaction: TransactionRawUpdate,
    db: Session = Depends(get_db)
):
    """Update a transaction."""
    try:
        db_transaction = db.query(TransactionRaw).filter(TransactionRaw.id == transaction_id).first()
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        update_data = transaction.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        logger.info(f"Transaction updated: {transaction_id}")
        return db_transaction
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update transaction")


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """Delete a transaction."""
    try:
        db_transaction = db.query(TransactionRaw).filter(TransactionRaw.id == transaction_id).first()
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        db.delete(db_transaction)
        db.commit()
        logger.info(f"Transaction deleted: {transaction_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete transaction")

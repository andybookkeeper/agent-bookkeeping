from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.receipt import Receipt
from backend.schemas.receipt import ReceiptCreate, ReceiptUpdate, ReceiptResponse
from backend.database import get_db
from backend.auth import authorize_api_request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/receipts",
    tags=["Receipts"],
    dependencies=[Depends(authorize_api_request)],
)


@router.get("/", response_model=List[ReceiptResponse])
async def list_receipts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    transaction_id: str = Query(None),
    db: Session = Depends(get_db)
):
    """List receipts with optional transaction filtering."""
    try:
        query = db.query(Receipt)
        if transaction_id:
            query = query.filter(Receipt.transaction_id == transaction_id)
        receipts = query.offset(skip).limit(limit).all()
        return receipts
    except SQLAlchemyError as e:
        logger.error(f"Database error listing receipts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch receipts")


@router.get("/{receipt_id}", response_model=ReceiptResponse)
async def get_receipt(receipt_id: str, db: Session = Depends(get_db)):
    """Get a specific receipt."""
    try:
        receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        return receipt
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching receipt: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch receipt")


@router.post("/", response_model=ReceiptResponse, status_code=201)
async def create_receipt(receipt: ReceiptCreate, db: Session = Depends(get_db)):
    """Create a new receipt."""
    try:
        db_receipt = Receipt(**receipt.dict())
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
        logger.info(f"Receipt created: {db_receipt.id}")
        return db_receipt
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating receipt: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create receipt")


@router.put("/{receipt_id}", response_model=ReceiptResponse)
async def update_receipt(
    receipt_id: str,
    receipt: ReceiptUpdate,
    db: Session = Depends(get_db)
):
    """Update a receipt."""
    try:
        db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not db_receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        
        update_data = receipt.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_receipt, key, value)
        
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
        logger.info(f"Receipt updated: {receipt_id}")
        return db_receipt
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating receipt: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update receipt")


@router.delete("/{receipt_id}", status_code=204)
async def delete_receipt(receipt_id: str, db: Session = Depends(get_db)):
    """Delete a receipt."""
    try:
        db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not db_receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        
        db.delete(db_receipt)
        db.commit()
        logger.info(f"Receipt deleted: {receipt_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting receipt: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete receipt")

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.payment import Payment
from backend.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from backend.database import get_db
from backend.auth import authorize_api_request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"],
    dependencies=[Depends(authorize_api_request)],
)


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    invoice_id: str = Query(None),
    db: Session = Depends(get_db)
):
    """List payments with optional invoice filtering."""
    try:
        query = db.query(Payment)
        if invoice_id:
            query = query.filter(Payment.invoice_id == invoice_id)
        payments = query.offset(skip).limit(limit).all()
        return payments
    except SQLAlchemyError as e:
        logger.error(f"Database error listing payments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch payments")


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str, db: Session = Depends(get_db)):
    """Get a specific payment."""
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch payment")


@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment."""
    try:
        db_payment = Payment(**payment.dict())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        logger.info(f"Payment created: {db_payment.id}")
        return db_payment
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create payment")


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: str,
    payment: PaymentUpdate,
    db: Session = Depends(get_db)
):
    """Update a payment."""
    try:
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        update_data = payment.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_payment, key, value)
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        logger.info(f"Payment updated: {payment_id}")
        return db_payment
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update payment")


@router.delete("/{payment_id}", status_code=204)
async def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    """Delete a payment."""
    try:
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        db.delete(db_payment)
        db.commit()
        logger.info(f"Payment deleted: {payment_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete payment")

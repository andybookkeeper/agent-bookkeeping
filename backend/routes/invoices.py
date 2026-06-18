from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.invoice import Invoice
from backend.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from backend.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/invoices", tags=["Invoices"])


@router.get("/", response_model=List[InvoiceResponse])
async def list_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    account_id: str = Query(None),
    db: Session = Depends(get_db)
):
    """List invoices with optional filtering."""
    try:
        query = db.query(Invoice)
        if status:
            query = query.filter(Invoice.status == status)
        if account_id:
            query = query.filter(Invoice.account_id == account_id)
        invoices = query.offset(skip).limit(limit).all()
        return invoices
    except SQLAlchemyError as e:
        logger.error(f"Database error listing invoices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch invoices")


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """Get a specific invoice."""
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching invoice: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch invoice")


@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    """Create a new invoice."""
    try:
        db_invoice = Invoice(**invoice.dict())
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        logger.info(f"Invoice created: {db_invoice.id}")
        return db_invoice
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating invoice: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create invoice")


@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: str,
    invoice: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    """Update an invoice."""
    try:
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        update_data = invoice.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_invoice, key, value)
        
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        logger.info(f"Invoice updated: {invoice_id}")
        return db_invoice
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating invoice: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update invoice")


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """Delete an invoice."""
    try:
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        db.delete(db_invoice)
        db.commit()
        logger.info(f"Invoice deleted: {invoice_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting invoice: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete invoice")

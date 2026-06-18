import logging
from backend.celery_config import celery_app
from backend.database import SessionLocal
from backend.models.invoice import Invoice, InvoiceStatus
from backend.models.receipt import Receipt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def process_invoice(self, invoice_id: str):
    """Process invoice and update status."""
    try:
        db = SessionLocal()
        try:
            invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
            if not invoice:
                logger.error(f"Invoice not found: {invoice_id}")
                return {"status": "failed", "message": "Invoice not found"}
            
            invoice.status = InvoiceStatus.SENT
            db.commit()
            logger.info(f"Invoice {invoice_id} processed successfully")
            return {"status": "success", "invoice_id": invoice_id}
        finally:
            db.close()
    except Exception as exc:
        logger.error(f"Error processing invoice {invoice_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=3)
def parse_receipt(self, receipt_id: str):
    """Parse receipt file and extract data."""
    try:
        db = SessionLocal()
        try:
            receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
            if not receipt:
                logger.error(f"Receipt not found: {receipt_id}")
                return {"status": "failed", "message": "Receipt not found"}
            
            logger.info(f"Parsing receipt {receipt_id} from {receipt.file_path}")
            
            return {
                "status": "success",
                "receipt_id": receipt_id,
                "parsed_data": {
                    "file": receipt.file_path,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        finally:
            db.close()
    except Exception as exc:
        logger.error(f"Error parsing receipt {receipt_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def check_overdue_invoices():
    """Check for overdue invoices and update their status."""
    try:
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            overdue_invoices = db.query(Invoice).filter(
                Invoice.due_date < now,
                Invoice.status != InvoiceStatus.PAID,
                Invoice.status != InvoiceStatus.CANCELLED
            ).all()
            
            for invoice in overdue_invoices:
                invoice.status = InvoiceStatus.OVERDUE
            
            db.commit()
            logger.info(f"Updated {len(overdue_invoices)} invoices to overdue")
            return {"status": "success", "updated_count": len(overdue_invoices)}
        finally:
            db.close()
    except Exception as exc:
        logger.error(f"Error checking overdue invoices: {str(exc)}")
        return {"status": "failed", "error": str(exc)}


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks."""
    sender.add_periodic_task(
        3600.0,
        check_overdue_invoices.s(),
        name="Check overdue invoices every hour"
    )

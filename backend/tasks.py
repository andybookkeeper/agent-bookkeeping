from celery import Celery
from config import settings

celery_app = Celery(
    "bookkeeping",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery_app.task
def process_invoice(invoice_id: int):
    """Process an invoice and update its status."""
    return {"invoice_id": invoice_id, "status": "processed"}


@celery_app.task
def parse_receipt(receipt_id: int, file_path: str):
    """Parse receipt file and extract information."""
    return {
        "receipt_id": receipt_id,
        "file_path": file_path,
        "status": "parsed",
    }


@celery_app.task
def generate_report(report_type: str, start_date: str, end_date: str):
    """Generate financial report."""
    return {
        "report_type": report_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": "generated",
    }

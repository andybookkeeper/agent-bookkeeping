import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse

from backend.database import engine
from backend.models.account import Base as AccountBase
from backend.models.journal_entry import Base as JournalEntryBase
from backend.models.transaction_raw import Base as TransactionBase
from backend.models.invoice import Base as InvoiceBase
from backend.models.payment import Base as PaymentBase
from backend.models.receipt import Base as ReceiptBase
from backend.routes import accounts, journal_entries, transactions, invoices, payments, receipts
from backend.utils.logging import get_logger

logger = get_logger(__name__)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000"
).split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    logger.info("Application startup")
    
    AccountBase.metadata.create_all(bind=engine)
    JournalEntryBase.metadata.create_all(bind=engine)
    TransactionBase.metadata.create_all(bind=engine)
    InvoiceBase.metadata.create_all(bind=engine)
    PaymentBase.metadata.create_all(bind=engine)
    ReceiptBase.metadata.create_all(bind=engine)
    
    yield
    
    logger.info("Application shutdown")


app = FastAPI(
    title="Agent Bookkeeping Platform",
    description="Full-stack agent-native bookkeeping system",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Agent Bookkeeping Platform"
    }


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint."""
    return {
        "message": "Agent Bookkeeping Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


app.include_router(accounts.router)
app.include_router(journal_entries.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(payments.router)
app.include_router(receipts.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("ENV") == "development"
    )

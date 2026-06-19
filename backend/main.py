import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from backend.database import engine
from backend.auth import validate_auth_settings
from backend.migrations.runner import run_migrations
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

    validate_auth_settings()

    auto_migrate = os.getenv("AUTO_MIGRATE", "true").lower() == "true"
    if auto_migrate:
        run_migrations(engine)
    else:
        logger.warning("AUTO_MIGRATE disabled; startup will not apply pending migrations")
    
    yield
    
    logger.info("Application shutdown")


app = FastAPI(
    title="Agent Bookkeeping Platform",
    description="Full-stack agent-native bookkeeping system",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
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

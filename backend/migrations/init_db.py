"""
Database initialization and migration helper
"""
import os
import logging
from sqlalchemy import text
from backend.database import engine, SessionLocal
from backend.models.account import Base as AccountBase
from backend.models.journal_entry import Base as JournalEntryBase
from backend.models.transaction_raw import Base as TransactionBase
from backend.models.invoice import Base as InvoiceBase
from backend.models.payment import Base as PaymentBase
from backend.models.receipt import Base as ReceiptBase

logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with all tables"""
    logger.info("Creating database tables...")
    
    AccountBase.metadata.create_all(bind=engine)
    JournalEntryBase.metadata.create_all(bind=engine)
    TransactionBase.metadata.create_all(bind=engine)
    InvoiceBase.metadata.create_all(bind=engine)
    PaymentBase.metadata.create_all(bind=engine)
    ReceiptBase.metadata.create_all(bind=engine)
    
    logger.info("Database tables created successfully")


def seed_sample_data():
    """Seed sample data for development"""
    from backend.models.account import Account, AccountType
    from datetime import datetime
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Account).first():
            logger.info("Database already contains data, skipping seed")
            return
        
        logger.info("Seeding sample data...")
        
        # Create sample accounts
        accounts = [
            Account(name="Cash", type=AccountType.ASSET, balance=10000.00),
            Account(name="Accounts Receivable", type=AccountType.ASSET, balance=5000.00),
            Account(name="Accounts Payable", type=AccountType.LIABILITY, balance=2000.00),
            Account(name="Retained Earnings", type=AccountType.EQUITY, balance=13000.00),
            Account(name="Sales Revenue", type=AccountType.REVENUE, balance=0.00),
            Account(name="Operating Expenses", type=AccountType.EXPENSE, balance=0.00),
        ]
        
        for account in accounts:
            db.add(account)
        
        db.commit()
        logger.info(f"Successfully created {len(accounts)} sample accounts")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding sample data: {str(e)}")
        raise
    finally:
        db.close()


def health_check():
    """Check database connectivity"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result:
                logger.info("Database health check: OK")
                return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    if health_check():
        init_database()
        seed_sample_data()
        logger.info("Database initialization complete")
    else:
        logger.error("Cannot initialize database - connection failed")

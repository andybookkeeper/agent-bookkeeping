from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.account import Account
from backend.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from backend.database import get_db
from backend.auth import authorize_api_request

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"],
    dependencies=[Depends(authorize_api_request)],
)


@router.get("/", response_model=List[AccountResponse])
async def list_accounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all accounts with pagination."""
    try:
        accounts = db.query(Account).offset(skip).limit(limit).all()
        return accounts
    except SQLAlchemyError as e:
        logger.error(f"Database error listing accounts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch accounts")


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str, db: Session = Depends(get_db)):
    """Get a specific account by ID."""
    try:
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch account")


@router.post("/", response_model=AccountResponse, status_code=201)
async def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """Create a new account."""
    try:
        db_account = Account(**account.dict())
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        logger.info(f"Account created: {db_account.id}")
        return db_account
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create account")


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    account: AccountUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing account."""
    try:
        db_account = db.query(Account).filter(Account.id == account_id).first()
        if not db_account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        update_data = account.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_account, key, value)
        
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        logger.info(f"Account updated: {account_id}")
        return db_account
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update account")


@router.delete("/{account_id}", status_code=204)
async def delete_account(account_id: str, db: Session = Depends(get_db)):
    """Delete an account."""
    try:
        db_account = db.query(Account).filter(Account.id == account_id).first()
        if not db_account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        db.delete(db_account)
        db.commit()
        logger.info(f"Account deleted: {account_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete account")

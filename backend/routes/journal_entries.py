from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.journal_entry import JournalEntry
from backend.schemas.journal_entry import JournalEntryCreate, JournalEntryUpdate, JournalEntryResponse
from backend.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/journal-entries", tags=["Journal Entries"])


@router.get("/", response_model=List[JournalEntryResponse])
async def list_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    account_id: str = Query(None),
    db: Session = Depends(get_db)
):
    """List journal entries with optional account filtering."""
    try:
        query = db.query(JournalEntry)
        if account_id:
            query = query.filter(JournalEntry.account_id == account_id)
        entries = query.offset(skip).limit(limit).all()
        return entries
    except SQLAlchemyError as e:
        logger.error(f"Database error listing entries: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch entries")


@router.get("/{entry_id}", response_model=JournalEntryResponse)
async def get_entry(entry_id: str, db: Session = Depends(get_db)):
    """Get a specific journal entry."""
    try:
        entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch entry")


@router.post("/", response_model=JournalEntryResponse, status_code=201)
async def create_entry(entry: JournalEntryCreate, db: Session = Depends(get_db)):
    """Create a new journal entry."""
    try:
        db_entry = JournalEntry(**entry.dict())
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        logger.info(f"Journal entry created: {db_entry.id}")
        return db_entry
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create entry")


@router.put("/{entry_id}", response_model=JournalEntryResponse)
async def update_entry(
    entry_id: str,
    entry: JournalEntryUpdate,
    db: Session = Depends(get_db)
):
    """Update a journal entry."""
    try:
        db_entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        update_data = entry.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_entry, key, value)
        
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        logger.info(f"Journal entry updated: {entry_id}")
        return db_entry
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update entry")


@router.delete("/{entry_id}", status_code=204)
async def delete_entry(entry_id: str, db: Session = Depends(get_db)):
    """Delete a journal entry."""
    try:
        db_entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        db.delete(db_entry)
        db.commit()
        logger.info(f"Journal entry deleted: {entry_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete entry")

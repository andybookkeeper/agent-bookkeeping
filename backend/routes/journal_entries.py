from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from backend.models.journal_entry import JournalEntry
from backend.schemas.journal_entry import (
    JournalEntryCreate,
    JournalEntryPairCreate,
    JournalEntryPairUpdate,
    JournalEntryUpdate,
    JournalEntryResponse,
)
from backend.database import get_db
from backend.auth import authorize_api_request
from backend.services.journal_service import (
    CreatePairInput,
    UpdatePairInput,
    create_journal_pair,
    update_journal_pair,
    delete_journal_pair,
)

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/journal-entries",
    tags=["Journal Entries"],
    dependencies=[Depends(authorize_api_request)],
)


@router.post("/legacy", deprecated=True, include_in_schema=True)
async def create_entry_legacy(_: JournalEntryCreate):
    """Deprecated legacy single-entry endpoint. Use strict pair posting on POST /api/journal-entries/."""
    raise HTTPException(
        status_code=410,
        detail="Legacy single-entry posting is deprecated. Use strict pair posting.",
    )


@router.put("/legacy/{entry_id}", deprecated=True, include_in_schema=True)
async def update_entry_legacy(entry_id: str, _: JournalEntryUpdate):
    """Deprecated legacy single-entry endpoint. Use strict pair posting on PUT /api/journal-entries/{entry_id}."""
    raise HTTPException(
        status_code=410,
        detail=f"Legacy single-entry update for {entry_id} is deprecated. Use strict pair posting.",
    )


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


@router.post("/", response_model=List[JournalEntryResponse], status_code=201)
async def create_entry(entry: JournalEntryPairCreate, db: Session = Depends(get_db)):
    """Create a strict double-entry journal pair."""
    try:
        debit_entry, credit_entry = create_journal_pair(
            db,
            CreatePairInput(
                date=entry.date,
                description=entry.description,
                debit_account_id=entry.debit_account_id,
                credit_account_id=entry.credit_account_id,
                amount=entry.amount,
            ),
        )
        logger.info("Journal pair created: %s", debit_entry.pair_id)
        return [debit_entry, credit_entry]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error creating entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create entry")


@router.put("/{entry_id}", response_model=List[JournalEntryResponse])
async def update_entry(
    entry_id: str,
    entry: JournalEntryPairUpdate,
    db: Session = Depends(get_db)
):
    """Update both sides of a strict journal pair using any entry in the pair."""
    try:
        debit_entry, credit_entry = update_journal_pair(
            db,
            entry_id,
            UpdatePairInput(
                date=entry.date,
                description=entry.description,
                amount=entry.amount,
            ),
        )
        logger.info(f"Journal pair updated via entry: {entry_id}")
        return [debit_entry, credit_entry]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error updating entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update entry")


@router.delete("/{entry_id}", status_code=204)
async def delete_entry(entry_id: str, db: Session = Depends(get_db)):
    """Delete both sides of a strict journal pair using any entry in the pair."""
    try:
        delete_journal_pair(db, entry_id)
        logger.info(f"Journal pair deleted via entry: {entry_id}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete entry")

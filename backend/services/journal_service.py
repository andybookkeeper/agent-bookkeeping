from dataclasses import dataclass
from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from backend.models.account import Account, AccountType
from backend.models.journal_entry import EntryType, JournalEntry


@dataclass
class CreateEntryInput:
    date: datetime
    description: str
    account_id: str
    amount: float
    entry_type: EntryType


@dataclass
class UpdateEntryInput:
    date: datetime | None = None
    description: str | None = None
    amount: float | None = None
    entry_type: EntryType | None = None


def _balance_delta(account_type: AccountType, entry_type: EntryType, amount: float) -> float:
    debit_increase = {AccountType.ASSET, AccountType.EXPENSE}
    credit_increase = {AccountType.LIABILITY, AccountType.EQUITY, AccountType.REVENUE}

    if entry_type == EntryType.DEBIT:
        return amount if account_type in debit_increase else -amount

    return amount if account_type in credit_increase else -amount


def _get_account_or_raise(db: Session, account_id: str) -> Account:
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Account not found")
    return account


def _get_entry_or_raise(db: Session, entry_id: str) -> JournalEntry:
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise ValueError("Entry not found")
    return entry


def _get_pair_or_raise(db: Session, pair_id: str) -> tuple[JournalEntry, JournalEntry]:
    entries = db.query(JournalEntry).filter(JournalEntry.pair_id == pair_id).all()
    if len(entries) != 2:
        raise ValueError("Invalid journal pair")

    debit = next((e for e in entries if e.type == EntryType.DEBIT), None)
    credit = next((e for e in entries if e.type == EntryType.CREDIT), None)
    if not debit or not credit:
        raise ValueError("Invalid journal pair")

    return debit, credit


def _validate_distinct_accounts(debit_account_id: str, credit_account_id: str) -> None:
    if debit_account_id == credit_account_id:
        raise ValueError("Debit and credit accounts must be different")


def _validate_pair_amount(debit_amount: float, credit_amount: float) -> None:
    if debit_amount <= 0 or credit_amount <= 0:
        raise ValueError("Amounts must be greater than zero")
    if abs(debit_amount - credit_amount) > 1e-9:
        raise ValueError("Debit and credit amounts must match")


def _apply_entry_balance(db: Session, entry: JournalEntry, factor: float) -> None:
    account = _get_account_or_raise(db, entry.account_id)
    delta = _balance_delta(account.type, entry.type, entry.amount) * factor
    account.balance += delta
    db.add(account)


@dataclass
class CreatePairInput:
    date: datetime
    description: str
    debit_account_id: str
    credit_account_id: str
    amount: float


@dataclass
class UpdatePairInput:
    date: datetime | None = None
    description: str | None = None
    amount: float | None = None


def create_journal_entry(db: Session, payload: CreateEntryInput) -> JournalEntry:
    account = _get_account_or_raise(db, payload.account_id)

    entry = JournalEntry(
        date=payload.date,
        description=payload.description,
        account_id=payload.account_id,
        amount=payload.amount,
        type=payload.entry_type,
    )

    delta = _balance_delta(account.type, entry.type, entry.amount)
    account.balance += delta

    try:
        db.add(entry)
        db.add(account)
        db.commit()
        db.refresh(entry)
        return entry
    except Exception:
        db.rollback()
        raise


def create_journal_pair(db: Session, payload: CreatePairInput) -> tuple[JournalEntry, JournalEntry]:
    _validate_distinct_accounts(payload.debit_account_id, payload.credit_account_id)
    _validate_pair_amount(payload.amount, payload.amount)

    _get_account_or_raise(db, payload.debit_account_id)
    _get_account_or_raise(db, payload.credit_account_id)

    pair_id = str(uuid.uuid4())
    debit_entry = JournalEntry(
        pair_id=pair_id,
        date=payload.date,
        description=payload.description,
        account_id=payload.debit_account_id,
        amount=payload.amount,
        type=EntryType.DEBIT,
    )
    credit_entry = JournalEntry(
        pair_id=pair_id,
        date=payload.date,
        description=payload.description,
        account_id=payload.credit_account_id,
        amount=payload.amount,
        type=EntryType.CREDIT,
    )

    try:
        db.add(debit_entry)
        db.add(credit_entry)
        _apply_entry_balance(db, debit_entry, factor=1.0)
        _apply_entry_balance(db, credit_entry, factor=1.0)
        db.commit()
        db.refresh(debit_entry)
        db.refresh(credit_entry)
        return debit_entry, credit_entry
    except Exception:
        db.rollback()
        raise


def update_journal_pair(db: Session, entry_id: str, payload: UpdatePairInput) -> tuple[JournalEntry, JournalEntry]:
    entry = _get_entry_or_raise(db, entry_id)
    if not entry.pair_id:
        raise ValueError("Entry is not part of a strict journal pair")

    debit_entry, credit_entry = _get_pair_or_raise(db, entry.pair_id)

    _apply_entry_balance(db, debit_entry, factor=-1.0)
    _apply_entry_balance(db, credit_entry, factor=-1.0)

    if payload.date is not None:
        debit_entry.date = payload.date
        credit_entry.date = payload.date
    if payload.description is not None:
        debit_entry.description = payload.description
        credit_entry.description = payload.description
    if payload.amount is not None:
        _validate_pair_amount(payload.amount, payload.amount)
        debit_entry.amount = payload.amount
        credit_entry.amount = payload.amount

    try:
        _apply_entry_balance(db, debit_entry, factor=1.0)
        _apply_entry_balance(db, credit_entry, factor=1.0)
        db.add(debit_entry)
        db.add(credit_entry)
        db.commit()
        db.refresh(debit_entry)
        db.refresh(credit_entry)
        return debit_entry, credit_entry
    except Exception:
        db.rollback()
        raise


def delete_journal_pair(db: Session, entry_id: str) -> None:
    entry = _get_entry_or_raise(db, entry_id)
    if not entry.pair_id:
        raise ValueError("Entry is not part of a strict journal pair")

    debit_entry, credit_entry = _get_pair_or_raise(db, entry.pair_id)

    _apply_entry_balance(db, debit_entry, factor=-1.0)
    _apply_entry_balance(db, credit_entry, factor=-1.0)

    try:
        db.delete(debit_entry)
        db.delete(credit_entry)
        db.commit()
    except Exception:
        db.rollback()
        raise


def update_journal_entry(db: Session, entry_id: str, payload: UpdateEntryInput) -> JournalEntry:
    entry = _get_entry_or_raise(db, entry_id)
    account = _get_account_or_raise(db, entry.account_id)

    original_delta = _balance_delta(account.type, entry.type, entry.amount)
    account.balance -= original_delta

    if payload.date is not None:
        entry.date = payload.date
    if payload.description is not None:
        entry.description = payload.description
    if payload.amount is not None:
        entry.amount = payload.amount
    if payload.entry_type is not None:
        entry.type = payload.entry_type

    updated_delta = _balance_delta(account.type, entry.type, entry.amount)
    account.balance += updated_delta

    try:
        db.add(entry)
        db.add(account)
        db.commit()
        db.refresh(entry)
        return entry
    except Exception:
        db.rollback()
        raise


def delete_journal_entry(db: Session, entry_id: str) -> None:
    entry = _get_entry_or_raise(db, entry_id)
    account = _get_account_or_raise(db, entry.account_id)

    delta = _balance_delta(account.type, entry.type, entry.amount)
    account.balance -= delta

    try:
        db.delete(entry)
        db.add(account)
        db.commit()
    except Exception:
        db.rollback()
        raise

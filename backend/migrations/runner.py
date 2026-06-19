import logging
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.engine import Engine

from backend.models.account import Base as AccountBase
from backend.models.invoice import Base as InvoiceBase
from backend.models.journal_entry import Base as JournalEntryBase
from backend.models.payment import Base as PaymentBase
from backend.models.receipt import Base as ReceiptBase
from backend.models.transaction_raw import Base as TransactionBase

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MigrationStep:
    version: str
    description: str


MIGRATIONS: list[MigrationStep] = [
    MigrationStep("0001_initial_schema", "Create initial bookkeeping tables"),
    MigrationStep("0002_journal_pair_id", "Add pair_id to journal entries"),
    MigrationStep("0003_enforce_pair_id_not_null", "Backfill and enforce non-null pair_id"),
]


def _ensure_migration_table(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(100) PRIMARY KEY,
                    description VARCHAR(255) NOT NULL,
                    applied_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
        )


def _is_applied(engine: Engine, version: str) -> bool:
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT 1 FROM schema_migrations WHERE version = :version"),
            {"version": version},
        ).first()
    return result is not None


def _record_migration(engine: Engine, step: MigrationStep) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO schema_migrations (version, description)
                VALUES (:version, :description)
                """
            ),
            {"version": step.version, "description": step.description},
        )


def _apply_step(engine: Engine, step: MigrationStep) -> None:
    if step.version == "0001_initial_schema":
        AccountBase.metadata.create_all(bind=engine)
        JournalEntryBase.metadata.create_all(bind=engine)
        TransactionBase.metadata.create_all(bind=engine)
        InvoiceBase.metadata.create_all(bind=engine)
        PaymentBase.metadata.create_all(bind=engine)
        ReceiptBase.metadata.create_all(bind=engine)
        return

    if step.version == "0002_journal_pair_id":
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    ALTER TABLE IF EXISTS journal_entries
                    ADD COLUMN IF NOT EXISTS pair_id VARCHAR(36)
                    """
                )
            )
            conn.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS ix_journal_entries_pair_id
                    ON journal_entries (pair_id)
                    """
                )
            )
        return

    if step.version == "0003_enforce_pair_id_not_null":
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    UPDATE journal_entries
                    SET pair_id = id
                    WHERE pair_id IS NULL
                    """
                )
            )
            conn.execute(
                text(
                    """
                    ALTER TABLE journal_entries
                    ALTER COLUMN pair_id SET NOT NULL
                    """
                )
            )
        return

    raise ValueError(f"Unknown migration step: {step.version}")


def run_migrations(engine: Engine) -> None:
    _ensure_migration_table(engine)

    for step in MIGRATIONS:
        if _is_applied(engine, step.version):
            continue

        logger.info("Applying migration %s: %s", step.version, step.description)
        _apply_step(engine, step)
        _record_migration(engine, step)
        logger.info("Migration %s applied", step.version)

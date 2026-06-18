import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bookkeeper:password@localhost:5432/bookkeeping"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=os.getenv("SQL_ECHO", "False").lower() == "true",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

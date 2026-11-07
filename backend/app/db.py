from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings, DEFAULT_DB_PATH

# Resolve database path relative to Path(__file__) and open SQLite read-only
db_file = DEFAULT_DB_PATH.resolve()

if settings.database_url and not settings.database_url.startswith("sqlite:///data/steam.db"):
    db_url = settings.database_url
else:
    # Use SQLite read-only URI mode
    db_url = f"sqlite:///file:{db_file.as_posix()}?mode=ro&uri=true"

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False, "uri": True} if "sqlite" in db_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

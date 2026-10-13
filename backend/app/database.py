import os
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from .config import PRODUCTION

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'desconfia_local.db'}"
DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL)
if DATABASE_URL.startswith(('postgres://', 'postgresql://')):
    DATABASE_URL = 'postgresql+psycopg://' + DATABASE_URL.split('://', 1)[1]
if PRODUCTION and not DATABASE_URL.startswith('postgresql'):
    raise RuntimeError('Produção exige PostgreSQL em DATABASE_URL.')

connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

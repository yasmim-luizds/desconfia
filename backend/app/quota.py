"""Persistent budgets shared by users/replicas connected to the same database.

Each admitted provider attempt consumes one unit, even if the provider fails.
This counts API attempts, not tokens or usage by scripts calling Groq directly.
"""
from time import time

from fastapi import HTTPException
from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from .config import AI_GLOBAL_PER_DAY, AI_GLOBAL_PER_MINUTE
from .models import AIQuota


def reserve_attempt(db: Session) -> None:
    now = int(time())
    dialect = db.get_bind().dialect.name
    insert = pg_insert if dialect == 'postgresql' else sqlite_insert
    try:
        # Stable lock order for concurrent PostgreSQL requests.
        for scope, seconds, limit in (
            ('global-day', 86400, AI_GLOBAL_PER_DAY),
            ('global-minute', 60, AI_GLOBAL_PER_MINUTE),
        ):
            start = now // seconds * seconds
            db.execute(insert(AIQuota).values(scope=scope, window_start=start, used=0)
                       .on_conflict_do_nothing(index_elements=['scope', 'window_start']))
            admitted = db.execute(update(AIQuota).where(
                AIQuota.scope == scope, AIQuota.window_start == start, AIQuota.used < limit,
            ).values(used=AIQuota.used + 1).returning(AIQuota.used)).scalar_one_or_none()
            if admitted is None:
                raise HTTPException(429, 'O limite compartilhado de análises foi atingido. Tente novamente mais tarde.',
                                    headers={'Retry-After': str(start + seconds - now),
                                             'X-Error-Code': 'ai_global_quota_exceeded'})
        db.execute(delete(AIQuota).where(AIQuota.window_start < now - 172800))
        # Commit before HTTP: no DB locks are held while waiting for Groq.
        db.commit()
    except Exception:
        db.rollback()
        raise

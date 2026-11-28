#!/bin/sh
set -eu
# Opt-in for one instance and a new/already versioned database only.
if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  python -m alembic upgrade head
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1

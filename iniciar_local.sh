#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if [[ ! -x .venv/bin/python ]]; then
  "$PYTHON_BIN" -m venv .venv
fi
source .venv/bin/activate
python -m pip install --disable-pip-version-check -q -r backend/requirements.txt
pnpm --dir frontend install --frozen-lockfile
pnpm --dir frontend build
cd "$ROOT_DIR/backend"

URL="http://127.0.0.1:8000"
printf '\nDesconfia pronto em %s\nPressione Ctrl+C para encerrar.\n' "$URL"
exec python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

"""Single-worker MVP limiter. Use a shared store before enabling multiple workers."""
from collections import OrderedDict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException

_entries = OrderedDict()
_lock = Lock()


def check_limit(key: str, limit: int):
    now = monotonic()
    with _lock:
        while _entries and next(iter(_entries.values()))[-1] <= now - 60:
            _entries.popitem(last=False)
        if key not in _entries and len(_entries) >= 10000:
            raise HTTPException(429, 'Muitas solicitações. Aguarde um minuto.', headers={'Retry-After': '60'})
        events = _entries.setdefault(key, deque())
        while events and events[0] <= now - 60:
            events.popleft()
        if len(events) >= limit:
            raise HTTPException(429, 'Muitas solicitações. Aguarde um minuto.', headers={'Retry-After': '60'})
        events.append(now)
        _entries.move_to_end(key)

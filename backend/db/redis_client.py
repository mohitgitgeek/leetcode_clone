"""Key-value persistence for CodeSage.

Uses Redis when it is reachable (e.g. via docker-compose), and transparently
falls back to an in-process dictionary when it is not, so the backend runs
locally with no Redis/Docker required.
"""
import os
import json

_backend = "memory"
_redis = None
_mem = {}

try:
    import redis as _redis_lib
    _candidate = _redis_lib.Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        db=0,
        socket_connect_timeout=1,
        decode_responses=True,
    )
    _candidate.ping()
    _redis = _candidate
    _backend = "redis"
except Exception:
    _redis = None
    _backend = "memory"


def backend_name():
    return _backend


def set_value(key, value):
    if _redis is not None:
        _redis.set(key, value)
    else:
        _mem[key] = value


def get_value(key):
    if _redis is not None:
        return _redis.get(key)
    return _mem.get(key)


def set_json(key, obj):
    set_value(key, json.dumps(obj))


def get_json(key, default=None):
    raw = get_value(key)
    if raw is None:
        return default
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return default


def cache_feedback(user_id, feedback):
    key = f"user:{user_id}:last_feedback"
    try:
        payload = feedback.model_dump_json()       # pydantic v2
    except AttributeError:
        payload = feedback.json()                  # pydantic v1
    set_value(key, payload)

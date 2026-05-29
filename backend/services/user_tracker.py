"""Tracks per-user progress and level, persisted via the key-value store."""
from db.redis_client import get_json, set_json


def get_stats(user_id: str):
    return get_json(f"user:{user_id}:stats", {
        "current_level": "Beginner",
        "recent_results": [],
        "total_submissions": 0,
        "total_passed": 0,
    })


def update_user_stats(user_id: str, passed: bool, level_up: bool):
    stats = get_stats(user_id)
    stats["total_submissions"] = stats.get("total_submissions", 0) + 1
    if passed:
        stats["total_passed"] = stats.get("total_passed", 0) + 1

    stats["recent_results"].append(bool(passed and level_up))
    stats["recent_results"] = stats["recent_results"][-3:]

    if stats["recent_results"].count(True) >= 3:
        if stats["current_level"] == "Beginner":
            stats["current_level"] = "Intermediate"
        elif stats["current_level"] == "Intermediate":
            stats["current_level"] = "Advanced"
        stats["recent_results"] = []

    set_json(f"user:{user_id}:stats", stats)
    return stats["current_level"]

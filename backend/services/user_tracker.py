user_stats = {}

def update_user_stats(user_id: str, passed: bool, level_up: bool):
    stats = user_stats.get(user_id, {
        "current_level": "Beginner",
        "recent_results": []
    })
    stats["recent_results"].append(passed and level_up)
    stats["recent_results"] = stats["recent_results"][-3:]
    if stats["recent_results"].count(True) >= 3:
        if stats["current_level"] == "Beginner":
            stats["current_level"] = "Intermediate"
        elif stats["current_level"] == "Intermediate":
            stats["current_level"] = "Advanced"
        stats["recent_results"] = []
    user_stats[user_id] = stats
    return stats["current_level"]

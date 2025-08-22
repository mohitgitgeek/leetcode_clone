import redis
from schemas import CodeFeedback

r = redis.Redis(host='redis', port=6379, db=0)

def cache_feedback(user_id: str, feedback: CodeFeedback):
    key = f"user:{user_id}:last_feedback"
    r.set(key, feedback.json())

from fastapi import APIRouter
from schemas import CodeSubmission, CodeFeedback
from services.ai_engine import analyze_code
from services.judge_engine import run_tests
from services.user_tracker import update_user_stats
from db.redis_client import cache_feedback

router = APIRouter()

@router.post("/submit", response_model=CodeFeedback)
async def submit_code(submission: CodeSubmission):
    ai_result = analyze_code(submission.code, submission.language)
    judge_result = run_tests(submission.code, submission.language)
    next_level = update_user_stats(submission.user_id, judge_result["passed"], ai_result["level_up"])
    combined_feedback = CodeFeedback(
        feedback=ai_result["feedback"],
        passed=judge_result["passed"],
        next_level=next_level
    )
    cache_feedback(submission.user_id, combined_feedback)
    return combined_feedback

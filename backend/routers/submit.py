from fastapi import APIRouter
from schemas import CodeSubmission, CodeFeedback
from services.ai_engine import analyze_code
from services.judge_engine import run_tests
from services.user_tracker import update_user_stats, get_stats
from db.redis_client import cache_feedback, backend_name

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "storage": backend_name()}


@router.get("/problem")
async def problem():
    import json
    import os
    from services.judge_engine import TEST_CASES_PATH
    try:
        with open(TEST_CASES_PATH) as f:
            data = json.load(f).get("python", {})
        return {
            "problem": data.get("problem", "Solve the problem."),
            "sample_input": data.get("input", ""),
            "expected_output": data.get("expected_output", ""),
        }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"problem": "Solve the problem.", "sample_input": "", "expected_output": ""}


@router.get("/stats/{user_id}")
async def stats(user_id: str):
    return get_stats(user_id)


@router.post("/submit", response_model=CodeFeedback)
async def submit_code(submission: CodeSubmission):
    ai_result = analyze_code(submission.code, submission.language)
    judge_result = run_tests(submission.code, submission.language)
    next_level = update_user_stats(submission.user_id, judge_result.get("passed", False), ai_result["level_up"])

    feedback_text = ai_result["feedback"]
    if judge_result.get("error"):
        feedback_text += f" (Runtime note: {judge_result['error']})"

    combined_feedback = CodeFeedback(
        feedback=feedback_text,
        passed=bool(judge_result.get("passed", False)),
        next_level=next_level,
        complexity_estimate=ai_result.get("complexity_estimate"),
        ml_difficulty=ai_result.get("ml_difficulty"),
        execution_time=judge_result.get("execution_time"),
        actual_output=judge_result.get("actual_output"),
        expected_output=judge_result.get("expected_output"),
    )
    cache_feedback(submission.user_id, combined_feedback)
    return combined_feedback

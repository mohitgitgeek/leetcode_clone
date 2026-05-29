from typing import Optional
from pydantic import BaseModel


class CodeSubmission(BaseModel):
    user_id: str
    code: str
    language: str


class CodeFeedback(BaseModel):
    feedback: str
    passed: bool
    next_level: str
    complexity_estimate: Optional[str] = None
    ml_difficulty: Optional[str] = None
    execution_time: Optional[float] = None
    actual_output: Optional[str] = None
    expected_output: Optional[str] = None

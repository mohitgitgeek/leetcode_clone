from pydantic import BaseModel

class CodeSubmission(BaseModel):
    user_id: str
    code: str
    language: str

class CodeFeedback(BaseModel):
    feedback: str
    passed: bool
    next_level: str

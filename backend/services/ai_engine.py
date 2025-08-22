import re

def analyze_code(code: str, language: str) -> dict:
    feedback_parts = []
    if re.search(r'for\s+.*:\s*\n\s*for\s+', code):
        complexity = "O(n^2)"
        feedback_parts.append("Consider optimizing nested loops to improve performance.")
        level_up = False
    elif any(fn in code for fn in ['sorted(', 'set(', 'heapq', 'deque']):
        complexity = "O(n log n)"
        feedback_parts.append("Good use of efficient built-in structures.")
        level_up = True
    else:
        complexity = "O(n)"
        feedback_parts.append("Simple logic detected; consider using better data structures.")
        level_up = True
    if len(code.split('\n')) < 5:
        feedback_parts.append("Try writing more modular code.")
    feedback_text = " ".join(feedback_parts)
    return {
        "complexity_estimate": complexity,
        "feedback": feedback_text,
        "level_up": level_up
    }

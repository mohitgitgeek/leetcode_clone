"""AI feedback engine for submitted code.

Combines lightweight static heuristics with a small scikit-learn model that
predicts a difficulty/complexity tier ("Easy" / "Medium" / "Hard") from
structural features of the code (length, loop nesting, recursion, use of
efficient data structures). The model is trained once on a synthetic, labelled
feature set, so there is no external data dependency. If scikit-learn is not
available the engine still returns useful rule-based feedback.
"""
import re

_model = None
_FEATURE_ORDER = ["lines", "loops", "max_nesting", "has_recursion", "uses_efficient"]


def _extract_features(code: str) -> dict:
    lines = [ln for ln in code.split("\n") if ln.strip()]
    loops = len(re.findall(r'\b(for|while)\b', code))
    # crude nesting estimate from leading indentation
    indents = [len(ln) - len(ln.lstrip()) for ln in lines] or [0]
    unit = min((i for i in indents if i > 0), default=4)
    max_nesting = max(indents) // unit if unit else 0
    has_recursion = 1 if re.search(r'def\s+(\w+)\s*\([^)]*\):[\s\S]*\b\1\s*\(', code) else 0
    uses_efficient = 1 if any(k in code for k in
                              ['sorted(', 'set(', 'dict(', 'heapq', 'deque', '{}', 'collections']) else 0
    return {
        "lines": len(lines), "loops": loops, "max_nesting": max_nesting,
        "has_recursion": has_recursion, "uses_efficient": uses_efficient,
    }


def _build_training_data(seed=11):
    import numpy as np
    rng = np.random.default_rng(seed)
    X, y = [], []
    for _ in range(900):
        lines = int(rng.integers(2, 60))
        loops = int(rng.integers(0, 5))
        nesting = int(rng.integers(0, 4))
        rec = int(rng.integers(0, 2))
        eff = int(rng.integers(0, 2))
        # Heuristic label: more loops/nesting/recursion => harder; efficiency lowers it a bit.
        score = loops * 1.0 + nesting * 1.3 + rec * 1.2 + lines * 0.03 - eff * 0.6
        label = 0 if score < 2.0 else (1 if score < 4.0 else 2)   # Easy / Medium / Hard
        X.append([lines, loops, nesting, rec, eff])
        y.append(label)
    return np.array(X, dtype=float), np.array(y)


def _get_model():
    global _model
    if _model is None:
        from sklearn.ensemble import RandomForestClassifier
        X, y = _build_training_data()
        clf = RandomForestClassifier(n_estimators=60, random_state=11)
        clf.fit(X, y)
        _model = clf
    return _model


def _ml_difficulty(features: dict):
    try:
        import numpy as np
        model = _get_model()
        x = np.array([[features[k] for k in _FEATURE_ORDER]], dtype=float)
        pred = int(model.predict(x)[0])
        return {0: "Easy", 1: "Medium", 2: "Hard"}[pred]
    except Exception:
        return None


def analyze_code(code: str, language: str) -> dict:
    feedback_parts = []
    features = _extract_features(code)

    if features["max_nesting"] >= 2 and features["loops"] >= 2:
        complexity = "O(n^2)"
        feedback_parts.append("Consider optimizing nested loops to improve performance.")
        level_up = False
    elif features["uses_efficient"]:
        complexity = "O(n log n)"
        feedback_parts.append("Good use of efficient built-in structures.")
        level_up = True
    else:
        complexity = "O(n)"
        feedback_parts.append("Simple logic detected; consider using better data structures.")
        level_up = True

    if features["lines"] < 5:
        feedback_parts.append("Try writing more modular code.")

    ml_difficulty = _ml_difficulty(features)
    if ml_difficulty:
        feedback_parts.append(f"ML difficulty estimate: {ml_difficulty}.")

    return {
        "complexity_estimate": complexity,
        "feedback": " ".join(feedback_parts),
        "level_up": level_up,
        "ml_difficulty": ml_difficulty,
    }

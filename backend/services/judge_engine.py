"""Runs submitted code against sample test cases.

Cross-platform: uses the current Python interpreter (sys.executable) rather than
a hard-coded "python3", and resolves the test-cases file relative to the backend
directory so it works regardless of the current working directory.
"""
import subprocess
import sys
import time
import uuid
import os
import json

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_CASES_PATH = os.path.join(BACKEND_DIR, "test_cases", "sample_input_output.json")


def run_tests(code: str, language: str):
    try:
        with open(TEST_CASES_PATH) as f:
            test_case = json.load(f).get(language)
    except FileNotFoundError:
        return {"passed": False, "error": "Test cases file not found."}

    if not test_case:
        return {"passed": False, "error": f"No test cases for language '{language}'."}

    filename = os.path.join(BACKEND_DIR, f"temp_{uuid.uuid4().hex}.{get_extension(language)}")
    with open(filename, "w") as f:
        f.write(code)
    try:
        start = time.time()
        output = execute_code(filename, test_case["input"], language)
        elapsed = round(time.time() - start, 4)
        passed = output.strip() == str(test_case["expected_output"]).strip()
        return {
            "passed": passed,
            "execution_time": elapsed,
            "actual_output": output,
            "expected_output": test_case["expected_output"],
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def get_extension(language):
    return {"python": "py", "c": "c", "cpp": "cpp", "java": "java"}.get(language, "txt")


def execute_code(filename, test_input, language):
    if language == "python":
        result = subprocess.run(
            [sys.executable, filename],
            input=test_input.encode(),
            capture_output=True,
            timeout=5,
        )
        if result.returncode != 0 and result.stderr:
            raise Exception(result.stderr.decode().strip())
        return result.stdout.decode()
    raise NotImplementedError(f"{language} not supported yet")

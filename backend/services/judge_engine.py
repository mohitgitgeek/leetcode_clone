import subprocess
import time
import uuid
import os
import json

TEST_CASES_PATH = "test_cases/sample_input_output.json"

def run_tests(code: str, language: str):
    with open(TEST_CASES_PATH) as f:
        test_case = json.load(f).get(language)
    if not test_case:
        return {"passed": False, "error": "No test cases for language."}
    filename = f"temp_{uuid.uuid4().hex}.{get_extension(language)}"
    with open(filename, "w") as f:
        f.write(code)
    try:
        start = time.time()
        output = execute_code(filename, test_case["input"], language)
        end = time.time()
        os.remove(filename)
        passed = output.strip() == test_case["expected_output"].strip()
        return {
            "passed": passed,
            "execution_time": round(end - start, 4),
            "actual_output": output
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}

def get_extension(language):
    return {"python": "py", "c": "c", "cpp": "cpp", "java": "java"}.get(language, "txt")

def execute_code(filename, test_input, language):
    if language == "python":
        result = subprocess.run(
            ["python3", filename],
            input=test_input.encode(),
            capture_output=True,
            timeout=2
        )
        if result.stderr:
            raise Exception(result.stderr.decode())
        return result.stdout.decode()
    raise NotImplementedError(f"{language} not supported yet")

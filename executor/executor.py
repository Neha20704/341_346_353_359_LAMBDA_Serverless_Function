# executor/executor.py
import subprocess
import os

def run_function(language, filename, timeout=5):
    """
    Execute a function inside a Docker container with timeout enforcement.

    Args:
        language (str): 'python' or 'javascript'
        filename (str): Function file name (e.g., hello.py)
        timeout (int): Timeout in seconds

    Returns:
        stdout (str), stderr (str)
    """
    container = f"lambda-{language}"
    func_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docker/functions", language))
   # func_path = os.path.abspath(f"./docker/functions/{language}")

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{func_path}:/functions",              # Mount host function dir to /functions in container
        "-e", f"FUNCTION_FILE={filename}",            # Pass the file to be run
        container                                     # This image runs handler.py/js, which picks up FUNCTION_FILE
    ]

    try:
        print("Running:", " ".join(cmd))  # Debug
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", f"ERROR: Execution timed out after {timeout} seconds"

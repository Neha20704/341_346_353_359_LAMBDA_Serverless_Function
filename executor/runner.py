import subprocess
import os
from queue import Queue

# Container pool setup
container_pool = Queue()
POOL_SIZE = 5

# List of functions to pre-warm
WARMED_FUNCTIONS = {
    "python": ["hello.py", "arithmetic.py", "infinite.py"],
    "javascript": ["hello.js", "arithmetic.js"]
}

def init_container_pool():
    for _ in range(POOL_SIZE):
        container_pool.put(None)  # Placeholder if you implement persistent containers

def run_function(language, filename, args=None, timeout=5):
    container = f"lambda-{language}"
    func_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docker/functions", language))

    # Build the base command
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{func_path}:/functions",
        "-e", f"FUNCTION_FILE={filename}",
    ]

    if args:
        import json
        cmd += ["-e", f"ARGS={json.dumps(args)}"]

    # Add image name last
    cmd.append(container)

    try:
        print("Running:", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", f"ERROR: Execution timed out after {timeout} seconds"
    except Exception as e:
        return "", f"ERROR: {str(e)}"
    finally:
        container_pool.put(None)

def warm_up_functions():
    print("Warming up frequently used functions...")
    for lang in WARMED_FUNCTIONS:
        for fname in WARMED_FUNCTIONS[lang]:
            try:
                print(f" → {lang}/{fname}")
                run_function(lang, fname, timeout=3)
            except Exception as e:
                print(f"Warm-up failed for {lang}/{fname}: {str(e)}")

# Init on import
init_container_pool()
warm_up_functions()

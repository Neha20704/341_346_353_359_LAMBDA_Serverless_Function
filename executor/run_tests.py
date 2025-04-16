# executor/run_tests.py
from executor import run_function

print("== Python Hello ==")
out, err = run_function("python", "hello.py", timeout=5)
print("Output:", out)
print("Error:", err)

print("== JavaScript Hello ==")
out, err = run_function("javascript", "hello.js", timeout=5)
print("Output:", out)
print("Error:", err)

print("== Timeout Test (infinite.py) ==")
out, err = run_function("python", "infinite.py", timeout=3)
print("Output:", out)
print("Error:", err)

print("== Error Test (bad file) ==")
out, err = run_function("python", "nonexistent.py", timeout=3)
print("Output:", out)
print("Error:", err)

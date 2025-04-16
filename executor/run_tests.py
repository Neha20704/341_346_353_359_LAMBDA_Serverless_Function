# executor/run_tests.py
from executor import run_function

print("== Python Hello ==")
out, err = run_function("python", "hello.py")
print("Output:", out)
print("Error:", err)

print("== JS Hello ==")
out, err = run_function("javascript", "hello.js")
print("Output:", out)
print("Error:", err)

print("== Timeout Test ==")
out, err = run_function("python", "infinite.py", timeout=3)
print("Output:", out)
print("Error:", err)

import sys

def add(a, b):
    return a + b

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python arithmetic.py <num1> <num2>")
    else:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        print(f"Sum: {add(num1, num2)}")

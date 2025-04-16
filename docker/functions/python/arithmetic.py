import sys

def add(a, b):
    return a + b

def main(arg1=None, arg2=None):
    if arg1 is None or arg2 is None:
        return "Usage: python arithmetic.py <num1> <num2>"
    try:
        num1 = float(arg1)
        num2 = float(arg2)
        return f"Sum: {add(num1, num2)}"
    except ValueError:
        return "Please provide valid numbers."

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print(main())  # Not enough arguments
    else:
        print(main(args[0], args[1]))

import sys

def main(name="World"):
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Get the name from CLI args
    arg = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(main(arg))

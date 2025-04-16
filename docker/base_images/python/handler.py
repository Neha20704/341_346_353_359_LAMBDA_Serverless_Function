import importlib.util
import os

func_file = os.environ.get("FUNCTION_FILE", "hello.py")

spec = importlib.util.spec_from_file_location("user_func", f"/functions/{func_file}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if hasattr(module, 'main'):
    print(module.main())
else:
    print("No main() found")

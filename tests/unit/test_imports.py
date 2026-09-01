import sys
import pathlib

print("=== Current working directory ===")
print(pathlib.Path.cwd())

print("\n=== Project structure ===")
for item in pathlib.Path(".").iterdir():
    print(f"  {item.name} ({'DIR' if item.is_dir() else 'FILE'})")

print("\n=== Trying imports ===")

# Method 1: Try from tests location
try:
    sys.path.insert(0, "/Users/bparlan/devcode/aef/agent")
    from core.validation import validate_metadata

    print("SUCCESS: Imported validate_metadata from /Users/bparlan/devcode/aef/agent")
except ImportError as exc:
    print(f"FAIL: validate_metadata from agent path: {exc}")

# Method 2: Try from tests location
try:
    sys.path.insert(0, "/Users/bparlan/devcode/aef/agent/tests")
    from core.validation import validate_metadata

    print("SUCCESS: Imported validate_metadata from tests path")
except ImportError as exc:
    print(f"FAIL: validate_metadata from tests path: {exc}")

# Method 3: Try relative to test file location
try:
    test_file = pathlib.Path(__file__)
    tests_dir = test_file.parent
    project_root = tests_dir.parent
    sys.path.insert(0, str(project_root))
    from core.validation import validate_metadata

    print(f"SUCCESS: Imported validate_metadata from {project_root}")
except ImportError as exc:
    print(f"FAIL: validate_metadata from relative path: {exc}")

# Method 4: Try core directly
try:
    sys.path.insert(0, "/Users/bparlan/devcode/aef/agent/core")
    from core.validation import validate_metadata

    print("SUCCESS: Imported validate_metadata from core directory")
except ImportError as exc:
    print(f"FAIL: validate_metadata from core directory: {exc}")

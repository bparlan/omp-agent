import sys
import pathlib

# Get the project root (where core/ is located)
repo_root = pathlib.Path(".").resolve()
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "core"))
sys.path.insert(0, str(repo_root / "core" / "artifacts"))

print("PATHS:", sys.path[:5])

try:
    from core.validation import validate_metadata

    print("SUCCESS: Imported validate_metadata")
except ImportError as exc:
    print(f"FAIL: validate_metadata import failed: {exc}")
    sys.exit(127)

# Test validation
try:
    result = validate_metadata("dummy.txt")
    print("SUCCESS: validate_metadata call succeeded")
    print("Result:", result)
except Exception as exc:
    print(f"FAIL: validate_metadata call failed: {exc}")
    sys.exit(1)

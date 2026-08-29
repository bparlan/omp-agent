import sys
import pathlib
import tempfile
import os

# Get the project root (where core/ is located)
repo_root = pathlib.Path('.').resolve()
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / 'core'))
sys.path.insert(0, str(repo_root / 'core' / 'artifacts'))

print("PATHS:", [p for p in sys.path if p])

try:
    from core.artifacts.resolution import resolve_artifact
    print("SUCCESS: Imported resolve_artifact")
except ImportError as exc:
    print(f"FAIL: resolve_artifact import failed: {exc}")
    sys.exit(127)

# Test 1: Check that the function has the correct signature
try:
    import inspect
    sig = inspect.signature(resolve_artifact)
    params = list(sig.parameters.keys())
    print(f"SUCCESS: resolve_artifact has signature: {sig}")

    # Check expected parameters
    expected_params = ['identity', 'artifact_type', 'metadata_filter', 'strict']
    for param in expected_params:
        if param not in params:
            print(f"FAIL: Expected parameter '{param}' not found in signature")
            sys.exit(1)

    print("SUCCESS: All expected parameters found")
except Exception as exc:
    print(f"FAIL: Signature check failed: {exc}")
    sys.exit(1)

# Test 2: Check that resolve_artifact returns proper structure for ambiguous resolution
try:
    # This should return an ambiguous resolution error since we have no artifacts
    result = resolve_artifact(artifact_type="specification", strict=True)

    if not isinstance(result, dict):
        print(f"FAIL: Expected dict result, got {type(result)}")
        sys.exit(1)

    if result.get("resolved") is not False:
        print(f"FAIL: Expected resolved=False for ambiguous/empty case, got {result.get('resolved')}")
        sys.exit(1)

    error = result.get("error")
    if not isinstance(error, dict):
        print(f"FAIL: Expected error dict, got {type(error)}")
        sys.exit(1)

    # Check that it has the expected structure for ambiguous resolution
    if error.get("type") != "AmbiguousResolutionError":
        print(f"FAIL: Expected error type 'AmbiguousResolutionError', got {error.get('type')}")
        sys.exit(1)

    print("SUCCESS: resolve_artifact returns proper structure for ambiguous resolution")
except Exception as exc:
    print(f"FAIL: Ambiguous resolution test failed: {exc}")
    sys.exit(1)

print("\nALL TESTS PASSED: resolve_artifact signature and structure are correct")

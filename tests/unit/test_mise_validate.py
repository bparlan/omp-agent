import sys
import os
sys.path.insert(0, '.')

# Import the mise_validate module
from mise_validate import validate_inner_config, validate_mise_config

# Test cases from the fixture
test_cases = [
    {
        "name": "Valid Python config",
        "config": {
            "environment": {
                "runtime": "python",
                "version": "3.11.0"
            },
            "tools": [
                {"name": "python", "version": "3.11.0"},
                {"name": "pip", "version": "22.0.0"}
            ]
        },
        "should_pass": True
    },
    {
        "name": "Invalid version format",
        "config": {
            "environment": {
                "runtime": "python",
                "version": "invalid-version"
            }
        },
        "should_pass": False
    },
    {
        "name": "Rust config with workspace",
        "config": {
            "environment": {
                "runtime": "rust",
                "version": "1.70.0"
            },
            "tools": [
                {"name": "rustc", "version": "1.70.0"},
                {"name": "cargo", "version": "1.70.0"}
            ],
            "workspace": {
                "isolation": True,
                "path": ".rust-env"
            }
        },
        "should_pass": True
    }
]

print("Testing mise-validate directly...")
for i, test_case in enumerate(test_cases):
    print(f"\nTest case {i+1}: {test_case['name']}")
    print(f"Config: {test_case['config']}")

    errors = validate_inner_config(test_case['config'])
    print(f"Errors: {errors}")

    if errors:
        print(f"FAILED: {len(errors)} validation errors")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"PASSED")

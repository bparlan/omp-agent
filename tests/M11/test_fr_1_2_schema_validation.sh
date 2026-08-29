#!/bin/bash
# test_fr_1_2_schema_validation.sh - Schema validation for FR-1.2 Mise Configuration schema contract
# Template Version: 1.0.0
# Expected Exit Code: 1 (baseline failure until implementation)

set -euo pipefail

TEST_NAME="FR-1.2 Mise Configuration Schema Validation"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-1.2.1,FR-1.2.2,FR-1.2.3,FR-1.2.4"

MISE_SCHEMA_CONTRACT='{
  "schema_version": "1.0.0",
  "mise_config": {
    "environment": {
      "runtime": {
        "type": "string",
        "enum": ["python", "node", "rust", "go", "deno", "common"],
        "required": true,
        "description": "Target runtime environment"
      },
      "version": {
        "type": "string",
        "required": true,
        "pattern": "^([0-9]+)\\.([0-9]+)\\.([0-9]+)([-+][a-zA-Z0-9]+)?$"
      }
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "version"],
        "properties": {
          "name": {"type": "string"},
          "version": {"type": "string"},
          "options": {"type": "object"},
          "env_vars": {"type": "object"}
        }
      }
    },
    "workspace": {
      "type": "object",
      "properties": {
        "isolation": {"type": "boolean", "default": true},
        "path": {"type": "string"},
        "permissions": {"type": "array", "items": {"type": "string"}}
      }
    },
    "cross_language": {
      "type": "object",
      "properties": {
        "compatibility_mode": {"type": "boolean", "default": false},
        "fallback_strategies": {"type": "array", "items": {"type": "string"}},
        "shared_components": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}'

MISE_FIXTURE='{
  "mise_config_validation": {
    "test_cases": [
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
        "should_pass": false
      },
      {
        "name": "Invalid version format",
        "config": {
          "environment": {
            "runtime": "python",
            "version": "invalid-version"
          }
        },
        "should_pass": true
      }
    ]
  }
}'

validate_schema_contract() {
    local schema_name="$1"
    local schema_content="$2"
    local fixture_content="$3"

    echo "Validating $schema_name schema contract..."

    if command -v python3 >/dev/null 2>&1; then
        local temp_schema=$(mktemp)
        local temp_fixture=$(mktemp)
        local temp_script=$(mktemp)

        echo "$schema_content" > "$temp_schema"
        echo "$fixture_content" > "$temp_fixture"

        cat > "$temp_script" << 'PYEOF'
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def validate_schema_contract(schema_path, fixture_path):
    try:
        import jsonschema
        from jsonschema import Draft7Validator
    except ImportError:
        print("ERROR: jsonschema package not installed")
        return False

    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        with open(fixture_path, 'r') as f:
            fixture = json.load(f)

        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(fixture))

        if errors:
            print(f"Schema validation failed with {len(errors)} errors:")
            for error in errors:
                print(f"  - {error.message}")
            return False
        else:
            print(f"Schema validation passed for {Path(schema_path).name}")
            return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema', required=True)
    parser.add_argument('--fixture', required=True)
    args = parser.parse_args()

    success = validate_schema_contract(args.schema, args.fixture)
    sys.exit(0 if success else 1)
PYEOF

        python3 "$temp_script" --schema "$temp_schema" --fixture "$temp_fixture"
        local validation_result=$?

        rm -f "$temp_schema" "$temp_fixture" "$temp_script"

        return $validation_result
    else
        echo "✗ python3 not available for schema validation"
        return 1
    fi
}

run_fr_1_2_schema_validation() {
    echo "Running FR-1.2 Mise Configuration Schema Validation Tests"
    echo "===================================================="

    if validate_schema_contract "fr1_2_mise_schema" "$MISE_SCHEMA_CONTRACT" "$MISE_FIXTURE"; then
        echo "✗ Schema validation unexpectedly succeeded (baseline expects failure)"
        return 1
    else
        echo "✓ Schema validation failed as expected (baseline behavior)"
        return 0
    fi
}

echo "Starting $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo ""

if run_fr_1_2_schema_validation; then
    echo "✓ FR-1.2 schema validation test completed"
else
    echo "✗ FR-1.2 schema validation test completed with expected failure"
fi

echo ""
echo "===================================================="
echo "Test Execution Summary for $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "Tests Run: FR-1.2 Mise Configuration Schema Validation"
echo "Expected Results: Schema validation fails (EXIT_CODE=1) - baseline behavior"
echo "===================================================="
exit 1

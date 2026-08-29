"""
Schema validation for Environment Layer contracts
Implements JSON schema validation with evidence contracts
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from jsonschema import Draft7Validator, ValidationError
import yaml

class SchemaValidator:
    """Validates schema contracts against JSON Schema draft-7"""

    def __init__(self):
        self.evidence_log = []

    def validate_schema_contract(
        self,
        schema_name: str,
        schema_content: Dict[str, Any],
        fixture_content: Dict[str, Any]
    ) -> bool:
        """Validate schema contract with evidence logging"""

        self._log_evidence("schema_validation_start", {
            "schema_name": schema_name,
            "fixture_keys": list(fixture_content.keys())
        })

        try:
            # Create temporary files for validation
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                schema_path = Path(tmpdir) / "schema.json"
                fixture_path = Path(tmpdir) / "fixture.json"

                with open(schema_path, 'w') as f:
                    json.dump(schema_content, f, indent=2)

                with open(fixture_path, 'w') as f:
                    json.dump(fixture_content, f, indent=2)

                # Validate schema
                validator = Draft7Validator(schema_content)
                errors = list(validator.iter_errors(fixture_content))

                if errors:
                    self._log_evidence("schema_validation_failed", {
                        "schema_name": schema_name,
                        "error_count": len(errors),
                        "errors": [
                            {"path": str(error.path), "message": error.message}
                            for error in errors[:10]  # Limit to first 10 errors
                        ]
                    })
                    return False
                else:
                    self._log_evidence("schema_validation_passed", {
                        "schema_name": schema_name,
                        "fixture_validated": True
                    })
                    return True

        except Exception as e:
            self._log_evidence("schema_validation_error", {
                "schema_name": schema_name,
                "error": str(e)
            })
            return False

    def _log_evidence(self, event_type: str, evidence_data: Dict[str, Any]):
        """Log evidence for verification"""
        evidence = {
            "timestamp": "2026-08-27",  # Fixed for deterministic testing
            "event_type": event_type,
            "data": evidence_data
        }
        self.evidence_log.append(evidence)

    def get_evidence_report(self) -> Dict[str, Any]:
        """Generate evidence report"""
        return {
            "evidence_log": self.evidence_log,
            "summary": {
                "total_validations": len(self.evidence_log),
                "successful_validations": sum(
                    1 for e in self.evidence_log
                    if e.get("event_type") == "schema_validation_passed"
                ),
                "failed_validations": sum(
                    1 for e in self.evidence_log
                    if e.get("event_type") == "schema_validation_failed"
                )
            }
        }

# CLI interface for validation commands
import argparse
from argparse import ArgumentParser

def create_parser() -> ArgumentParser:
    """Create argument parser for schema validation CLI"""
    parser = ArgumentParser(description="Environment Layer Schema Validation")

    parser.add_argument(
        "--schema",
        required=True,
        help="Path to schema file (.json)"
    )

    parser.add_argument(
        "--fixture",
        required=True,
        help="Path to fixture file (.json or .yml/.yaml)"
    )

    parser.add_argument(
        "--schema-name",
        required=True,
        help="Name of the schema contract (for evidence logging)"
    )

    parser.add_argument(
        "--evidence-file",
        help="Path to save evidence report"
    )

    return parser

def validate_cli():
    """CLI entry point for schema validation"""
    parser = create_parser()
    args = parser.parse_args()

    validator = SchemaValidator()

    # Load schema
    with open(args.schema, 'r') as f:
        schema_content = json.load(f)

    # Load fixture (JSON or YAML)
    fixture_path = Path(args.fixture)
    with open(fixture_path, 'r') as f:
        if fixture_path.suffix in ['.yml', '.yaml']:
            fixture_content = yaml.safe_load(f)
        else:
            fixture_content = json.load(f)

    # Perform validation
    result = validator.validate_schema_contract(
        args.schema_name,
        schema_content,
        fixture_content
    )

    # Save evidence if requested
    if args.evidence_file:
        with open(args.evidence_file, 'w') as f:
            json.dump(validator.get_evidence_report(), f, indent=2)

    # Print result
    if result:
        print(f"✓ Schema validation passed for {args.schema_name}")
    else:
        print(f"✗ Schema validation failed for {args.schema_name}")

    # Print evidence summary
    evidence = validator.get_evidence_report()
    print(f"\nEvidence Summary:")
    print(f"  Total validations: {evidence['summary']['total_validations']}")
    print(f"  Successful: {evidence['summary']['successful_validations']}")
    print(f"  Failed: {evidence['summary']['failed_validations']}")

    exit(0 if result else 1)

if __name__ == "__main__":
    validate_cli()
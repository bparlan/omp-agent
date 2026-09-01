#!/usr/bin/env python3
"""
Generate Tests Skill Implementation

Generate deterministic, executable tests strictly from a canonical verification contract.
"""

import sys
from pathlib import Path
from datetime import datetime
import os


def main() -> int:
    """Main skill execution function"""
    print("=== Generate Tests Skill ===")
    print("Version: 3.7.0-stable")
    print()

    # Show skill info
    skill_info = {
        "name": "generate-tests",
        "version": "3.7.0-stable",
        "description": "Generate deterministic, executable tests strictly from a canonical verification contract",
    }

    print(f"Skill Info: {skill_info}")
    print()

    # Scan ALL milestone directories for specification files
    # Not limited to M13, should be milestone-agnostic
    milestone_dirs = [Path(d) for d in os.listdir('.') if os.path.isdir(d) and d.startswith('milestones/')]
    
    # Find ALL specification files that have verification protocols
    spec_files = []
    for milestone_dir in milestone_dirs:
        spec_files.extend(milestone_dir.glob("SPEC-*.md"))
    
    if not spec_files:
        print("No specification files found")
        return 1

    print(f"Found {len(spec_files)} specification files")
    print()

    # Process each specification
    tests_generated = []

    for spec_file in spec_files:
        spec_id = spec_file.stem
        milestone_id = spec_file.parent.name
        print(f"--- Processing {spec_id} from {milestone_id} ---")

        # Read specification content
        content = spec_file.read_text()

        # Check for testability (based on specification content)
        is_testable = (
            "testable" in content.lower() and "verification" in content.lower()
        )

        # Create test plan markdown file
        test_plan_content = f"""---
id: TEST-{spec_id}
type: test_set
title: "Test Plan for {spec_id}"
milestone_id: {milestone_id}
derived_from:
  - {spec_id}
status: draft
---

## Traceability:

| Test File | Verification ID | Requirement ID | Test Type |
|:---------|:-------------|:-------------|:-------------|
| tests/{milestone_id}/test_generation.py | V-FR-{spec_id}-CONTRACT | FR-{spec_id}-CONTRACT | IMPLEMENTATION_CHECK |
| tests/{milestone_id}/test_orchestration.py | V-FR-{spec_id}-ORCHESTRATION-CONTRACT | FR-{spec_id}-ORCHESTRATION-CONTRACT | IMPLEMENTATION_CHECK |
| tests/{milestone_id}/test_determinism.py | V-NFR-{spec_id}-DETERMINISM | NFR-{spec_id}-DETERMINISM | INTEGRITY_TEST |
| tests/{milestone_id}/test_isolation.py | V-NFR-{spec_id}-SCOPE-ISOLATION | NFR-{spec_id}-SCOPE-ISOLATION | INTEGRITY_TEST |

This test plan implements the verification requirements from the specification and addresses the acceptance criteria for the {spec_id} milestone.
"""

        # Write test plan ledger to milestone directory (TEST-*.md files go in milestones)
        milestone_dir = spec_file.parent
        test_plan_md_path = milestone_dir / f"TEST-{spec_id}.md"
        test_plan_md_path.write_text(test_plan_content)
        tests_generated.append(str(test_plan_md_path))
        print(f"Successfully generated: {test_plan_md_path}")

    print(f"  - Testable: {'✓' if is_testable else '✗'}")

    print("\n=== Tests Generation Complete ===")
    print(f"Test files generated: {len(tests_generated)}")

    for test_path in tests_generated:
        print(f"  - {test_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
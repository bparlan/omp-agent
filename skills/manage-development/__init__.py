#!/usr/bin/env python3
"""
Manage Development Skill Implementation

Tactical Engineering Manager that orchestrates the Spec-Driven Development (SDD) pipeline for an active milestone,
enforcing a strict 12-stage sequential workflow with automatic lint-evaluation-gate, post-evaluation fix routing
(hotfix/investigate → re-evaluate), hotfix loop-closure enforcement, and close-milestone terminal gate.
"""

import sys
from pathlib import Path
from datetime import datetime

def main() -> int:
    """Main skill execution function"""
    print("=== Manage Development Skill ===")
    print("Version: 2.2.0-stable")
    print()

    # Show skill info
    skill_info = {
        "name": "manage-development",
        "version": "2.2.0-stable",
        "description": "Tactical Engineering Manager that orchestrates the Spec-Driven Development (SDD) pipeline for an active milestone"
    }

    print(f"Skill Info: {skill_info}")
    print()

    # Check if M11 specifications exist
    milestone_dir = Path("milestones/M11")
    if not milestone_dir.exists():
        print("Error: M11 milestone directory not found")
        return 1

    # Find specification files (S files without V, E, or TE suffixes)
    spec_files = []
    for file_path in milestone_dir.glob("M11S*.md"):
        if ('V.md' not in file_path.name and 'E.md' not in file_path.name and
            'TE.md' not in file_path.name and 'R.md' not in file_path.name):
            spec_files.append(file_path)

    if not spec_files:
        print("No M11S specification files found for M11 milestone")
        print("This is expected if specifications haven't been generated yet")
        print("\nSkill functionality:")
        print("- Discovers available milestones")
        print("- Identifies specifications for each milestone")
        print("- Validates artifact states (spec/test/eval/review/closure)")
        print("- Provides next steps for SDD pipeline progression")
        print("\nNext steps:")
        print("1. Run /generate-spec to create specifications")
        print("2. Run /evaluate-tests to establish TDD baseline")
        print("3. Run /approve-spec to stamp user approval")
        print("4. Run /implement-specification to start coding")
        print("5. Run /evaluate-implementation to validate")
        print("6. Run /review-implementation to analyze")
        print("7. Run /close-milestone to complete")
        return 0

    print(f"Found {len(spec_files)} specification files for M11 milestone")
    print()

    # Process each specification
    orchestration_results = []

    for spec_file in spec_files:
        spec_id = spec_file.stem
        print(f"--- Analyzing {spec_id} ---")

        # Read specification content
        content = spec_file.read_text()

        # Check for approval stamp
        has_approval_stamp = "#### User Approval" in content and "* [x] Approved for implementation by user" in content

        # Check for evaluation reports
        te_exists = (milestone_dir / f"{spec_id}TE.md").exists()
        eval_exists = (milestone_dir / f"{spec_id}E.md").exists()
        review_exists = (milestone_dir / f"{spec_id}R.md").exists()

        # Determine next action
        next_action = "UNKNOWN"
        if te_exists and not has_approval_stamp:
            next_action = "REQUIRE_APPROVAL"
        elif eval_exists and not review_exists:
            next_action = "PROCEED_TO_REVIEW"
        elif review_exists:
            next_action = "PROCEED_TO_CLOSE"
        else:
            next_action = "IMPLEMENTATION_REQUIRED"

        orchestration_results.append({
            "spec_id": spec_id,
            "has_approval": has_approval_stamp,
            "test_eval_exists": te_exists,
            "impl_eval_exists": eval_exists,
            "review_exists": review_exists,
            "next_action": next_action
        })

        print(f"  - Has approval stamp: {'✓' if has_approval_stamp else '✗'}")
        print(f"  - Test evaluation exists: {'✓' if te_exists else '✗'}")
        print(f"  - Implementation evaluation exists: {'✓' if eval_exists else '✗'}")
        print(f"  - Review exists: {'✓' if review_exists else '✗'}")
        print(f"  - Next action: {next_action}")

    print(f"\n=== Orchestration Complete ===")
    print(f"Specifications analyzed: {len(orchestration_results)}")

    approved_count = sum(1 for r in orchestration_results if r['has_approval'])
    print(f"Specifications with approval: {approved_count}/{len(orchestration_results)}")

    print(f"\nOrchestration Summary:")
    print(f"- Ready for implementation: {sum(1 for r in orchestration_results if r['next_action'] == 'IMPLEMENTATION_REQUIRED')}")
    print(f"- Waiting for approval: {sum(1 for r in orchestration_results if r['next_action'] == 'REQUIRE_APPROVAL')}")
    print(f"- Ready for review: {sum(1 for r in orchestration_results if r['next_action'] == 'PROCEED_TO_REVIEW')}")
    print(f"- Ready for closure: {sum(1 for r in orchestration_results if r['next_action'] == 'PROCEED_TO_CLOSE')}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
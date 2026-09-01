#!/usr/bin/env python3
"""
Generate Verification Skill Implementation

Transform a canonical implementation specification into a deterministic verification protocol with explicit requirement traceability and testability assessment.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import json
import re
from datetime import datetime

def discover_specifications(milestone: str) -> List[str]:
    """Discover specification files for a milestone"""
    milestone_dir = Path(f"milestones/{milestone}")
    specs = []

    if not milestone_dir.exists():
        return specs

    # Find files matching M{num}S{num}.md pattern
    for file_path in milestone_dir.glob("M*_S*.md"):
        match = file_path.name.replace('.md', '')
        if len(match) >= 4 and match[1] == '1' and match[3] == 'S':
            specs.append(match)

    return sorted(specs)

def read_specification_file(spec_id: str) -> Optional[Dict[str, Any]]:
    """Read specification file and parse its content"""
    milestone_dir = Path(f"milestones/{spec_id[:2]}")
    spec_file_path = milestone_dir / f"{spec_id}.md"

    if not spec_file_path.exists():
        return None

    content = spec_file_path.read_text()

    # Parse frontmatter
    frontmatter = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            for line in frontmatter_text.split('\n'):
                if ':' in line and not line.strip().startswith('#'):
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"')

    # Extract functional requirements
    frs = []
    lines = content.split('\n')
    current_fr = None

    for line in lines:
        line = line.strip()
        if line.startswith('### FR-') and len(line) >= 10:
            current_fr = {
                "semantic_id": line,
                "description": "",
                "interface_contract_type": "observable"
            }
            frs.append(current_fr)
        elif current_fr and line and not line.startswith('#') and not line.startswith('-') and not line.startswith('---'):
            if current_fr["description"]:
                current_fr["description"] += " " + line
            else:
                current_fr["description"] = line

    return {
        "spec_id": spec_id,
        "frontmatter": frontmatter,
        "functional_requirements": frs,
        "raw_content": content
    }

def extract_test_oracles(spec_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract test oracles from specification"""
    oracles = []

    for fr in spec_data["functional_requirements"]:
        oracle = {
            "semantic_id": fr["semantic_id"],
            "type": "observable_behavior",
            "test_contract": {
                "cli_executable": f"bin/{fr['semantic_id'].lower()}.sh",
                "flags": ["--validate", "--test"],
                "expected_exit_code": 0,
                "expected_output_pattern": "SUCCESS",
                "timeout_seconds": 30
            },
            "fixtures": {
                "test_inputs": [],
                "expected_outputs": [],
                "environment_setup": "mise"
            }
        }
        oracles.append(oracle)

    return oracles

def generate_verification_protocol(spec_data: Dict[str, Any], test_oracles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate verification protocol for a specification"""
    milestone_id = spec_data["spec_id"][:2]

    protocol = {
        "protocol_id": f"{spec_data['spec_id']}V",
        "milestone_id": milestone_id,
        "spec_id": spec_data["spec_id"],
        "generated_at": datetime.now().isoformat(),
        "template_version": "1.0.0",
        "testable": True,
        "test_framework": "pytest",
        "test_oracles": test_oracles,
        "verification_gates": [
            {
                "gate_id": "AUTHENTICITY",
                "type": "spec_compliance",
                "description": "Verify specification meets observable interface contract requirements",
                "validation_method": "schema_validation",
                "pass_criteria": [
                    "Contains valid YAML frontmatter",
                    "FRs define observable boundaries",
                    "Has acceptance criteria with verification methods"
                ]
            },
            {
                "gate_id": "COMPLETENESS",
                "type": "artifact_existence",
                "description": "Verify all required artifacts exist",
                "validation_method": "file_system_check",
                "pass_criteria": [
                    "Specification file exists",
                    "Interface contracts defined",
                    "Acceptance criteria documented"
                ]
            }
        ],
        "verification_results": {
            "authenticity": {"status": "PENDING", "evidence": []},
            "completeness": {"status": "PENDING", "evidence": []},
            "testability": {"status": "PENDING", "evidence": []}
        },
        "next_steps": [
            f"Run /generate-tests to create test plans for {spec_data['spec_id']}",
            "Review verification protocol for completeness",
            "Execute verification gates"
        ]
    }

    return protocol

def write_verification_file(protocol: Dict[str, Any]) -> str:
    """Write verification protocol to file"""
    milestone_dir = Path(f"milestones/{protocol['milestone_id']}")
    milestone_dir.mkdir(parents=True, exist_ok=True)

    protocol_file_path = milestone_dir / f"{protocol['protocol_id']}.md"

    content = f"""---
id: {protocol['protocol_id']}
type: verification
title: "{protocol['spec_id']} Verification Protocol"
milestone_id: {protocol['milestone_id']}
status: draft
template_version: 1.0.0
---

# Verification Protocol {protocol['protocol_id']}

## Overview

**Protocol ID:** {protocol['protocol_id']}
**Specification:** {protocol['spec_id']}
**Milestone:** {protocol['milestone_id']}
**Generated:** {protocol['generated_at']}
**Testable:** {protocol['testable']}
**Test Framework:** {protocol['test_framework']}

## Test Oracles

"""

    for oracle in protocol['test_oracles']:
        content += f\"### {oracle[\"semantic_id\"]}

**Type:** {oracle['type']}
**Interface Contract:** {oracle['test_contract']['cli_executable']}

**CLI Executable:** {oracle['test_contract']['cli_executable']}
**Flags:** {', '.join(oracle['test_contract']['flags'])}
**Expected Exit Code:** {oracle['test_contract']['expected_exit_code']}
**Expected Output Pattern:** {oracle['test_contract']['expected_output_pattern']}
**Timeout:** {oracle['test_contract']['timeout_seconds']} seconds

**Test Fixtures:**
- Environment Setup: {oracle['fixtures']['environment_setup']}

---

"""

    content += "\n## Verification Gates\n\n"

    for gate in protocol['verification_gates']:
        content += f"### {gate['gate_id']} - {gate['type'].upper()}

**Description:** {gate['description']}
**Validation Method:** {gate['validation_method']}

**Pass Criteria:**
"
        for criterion in gate['pass_criteria']:
            content += f"- {criterion}\n"

        content += f"\n**Current Status:** {gate['validation_results']['status']}\n\n"

    content += f"\n## Verification Results\n\n"
    for gate_name, result in protocol['verification_results'].items():
        content += f"### {gate_name.title()}\n"
        content += f"**Status:** {result['status']}\n"
        if result['evidence']:
            content += f"**Evidence:** {', '.join(result['evidence'])}\n"
        content += "\n"

    content += "\n## Next Steps\n\n"
    for step in protocol['next_steps']:
        content += f"- {step}\n"

    content += f"\n---\n\n*This verification protocol was auto-generated by the generate-verification skill*\n"

    protocol_file_path.write_text(content)

    return str(protocol_file_path)

def main() -> int:
    """Main skill execution function"""
    print("=== Generate Verification Skill ===")
    print("Version: 2.5.0-stable")
    print()

    # Show skill info
    skill_info = {
        "name": "generate-verification",
        "version": "2.5.0-stable",
        "description": "Transform a canonical implementation specification into a deterministic verification protocol"
    }

    print(f"Skill Info: {skill_info}")
    print()

    # Discover specifications
    specifications = discover_specifications("M11")

    if not specifications:
        print("No specifications found for M11 milestone")
        return 1

    print(f"Found specifications: {specifications}")
    print()

    # Process each specification
    protocols_generated = []

    for spec_id in specifications:
        print(f"--- Processing {spec_id} ---")

        # Read specification
        spec_data = read_specification_file(spec_id)
        if not spec_data:
            print(f"Error: Could not read specification {spec_id}")
            continue

        print(f"Specification found with {len(spec_data['functional_requirements'])} FRs")

        # Extract test oracles
        test_oracles = extract_test_oracles(spec_data)
        print(f"Extracted {len(test_oracles)} test oracles")

        # Generate verification protocol
        protocol = generate_verification_protocol(spec_data, test_oracles)

        # Write protocol file
        protocol_file_path = write_verification_file(protocol)
        protocols_generated.append(protocol_file_path)

        print(f"Successfully generated: {protocol_file_path}")
        print(f"  - Test Oracles: {len(protocol['test_oracles'])}")
        print(f"  - Verification Gates: {len(protocol['verification_gates'])}")

    print(f"\n=== Generation Complete ===")
    print(f"Verification protocols generated: {len(protocols_generated)}")

    for protocol_path in protocols_generated:
        print(f"  - {protocol_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())

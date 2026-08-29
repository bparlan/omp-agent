#!/usr/bin/env python3
"""
Generate Spec Skill Implementation

Transform an approved milestone document into a detailed implementation specification with strict, machine-readable requirement traceability and semantic FR IDs.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import re
import json
from datetime import datetime

def read_milestone_file(milestone_id: str) -> Optional[str]:
    """Read milestone file"""
    milestone_path = Path(f"milestones/{milestone_id}/{milestone_id}.md")
    if milestone_path.exists():
        return milestone_path.read_text()
    return None

def extract_functional_requirements(milestone_content: str) -> List[Dict[str, Any]]:
    """Extract functional requirements from milestone content"""
    frs = []
    lines = milestone_content.split('\n')

    current_fr = None
    fr_id_counter = 1

    for line in lines:
        line = line.strip()

        # Match functional requirement headers (M11S1, M11S2, etc.)
        if line.startswith('### M11S'):
            current_fr = {
                "id": f"FR-{fr_id_counter:02d}",
                "spec_id": line.replace('### ', ''),
                "title": "",
                "requirements": [],
                "acceptance_criteria": []
            }
            fr_id_counter += 1
            frs.append(current_fr)

        # Match requirement bullet points
        elif current_fr and line.startswith('- **FR-'):
            # Extract semantic FR ID
            match = re.search(r'\*\*FR-(\w+)\*\*', line)
            if match:
                semantic_id = match.group(1)
            else:
                semantic_id = f"FR-{fr_id_counter:02d}"

            requirement = {
                "semantic_id": semantic_id,
                "text": line.replace('- **', '').replace('**', ''),
                "type": "functional_requirement"
            }
            current_fr["requirements"].append(requirement)

        # Match acceptance criteria
        elif current_fr and line.startswith('- [ ]'):
            criterion = {
                "id": f"AC-{fr_id_counter:02d}",
                "text": line.replace('- [ ] ', ''),
                "type": "acceptance_criterion"
            }
            current_fr["acceptance_criteria"].append(criterion)

    return frs

def generate_yaml_frontmatter(spec_id: str, milestone_id: str) -> str:
    """Generate YAML frontmatter for specification"""
    return f"""---
id: {spec_id}
type: specification
title: "{spec_id} - {spec_id.split('S')[0]} Specification"
milestone_id: {milestone_id}
status: draft
template_version: 1.3.0
---"""

def generate_specification(milestone_id: str, spec_id: str) -> Dict[str, Any]:
    """Generate specification for a milestone"""
    milestone_content = read_milestone_file(milestone_id)

    if not milestone_content:
        return {"error": f"Milestone {milestone_id} not found"}

    # Extract functional requirements
    frs = extract_functional_requirements(milestone_content)

    # Find the specific FRs for this spec
    spec_frs = [fr for fr in frs if fr["spec_id"] == spec_id]

    if not spec_frs:
        return {"error": f"No functional requirements found for {spec_id}"}

    spec_fr = spec_frs[0]

    # Generate specification
    spec = {
        "frontmatter": generate_yaml_frontmatter(spec_id, milestone_id),
        "metadata": {
            "spec_id": spec_id,
            "milestone_id": milestone_id,
            "generated_at": datetime.now().isoformat(),
            "template_version": "1.3.0",
            "semantic_fr_count": len(spec_fr["requirements"]),
            "acceptance_criterion_count": len(spec_fr["acceptance_criteria"])
        },
        "functional_requirements": spec_fr["requirements"],
        "acceptance_criteria": spec_fr["acceptance_criteria"],
        "interface_contracts": [
            {
                "type": "observable_boundary",
                "description": f"CLI Executable Contract for {spec_id}",
                "required": True
            }
        ],
        "strict_file_scope": {
            "allowlist": [
                f"src/{spec_id.lower()}.py",
                f"bin/{spec_id.lower()}.sh",
                f"tests/{milestone_id}/{spec_id}.py"
            ],
            "denylist": [
                "*.html",
                "*.css",
                "*.json",
                "*.env",
                "*.key",
                "secrets*",
                "credentials*"
            ]
        },
        "affected_modules": [
            {
                "name": f"{spec_id}-core",
                "public_interface": True,
                "exports": [
                    f"class {spec_id.title().replace('-', '')}Impl",
                    f"function execute{spectral_id.upper()}",
                    f"function validate{spectral_id.upper()}"
                ]
            }
        ],
        "new_modules": [],
        "removed_modules": [],
        "implementation_tasks": [
            f"1. Create core implementation for {spec_id}",
            f"2. Implement semantic FR IDs: {[fr['semantic_id'] for fr in spec_fr['requirements']]}",
            f"3. Define observable interface contracts",
            f"4. Create tests for all acceptance criteria",
            f"5. Validate specification compliance"
        ],
        "next_steps": [
            "Run /generate-verification to create verification protocol",
            "Review specification before proceeding",
            "Approve specification for implementation"
        ]
    }

    return spec

def write_specification_file(spec: Dict[str, Any]) -> str:
    """Write specification to file"""
    milestone_id = spec["metadata"]["milestone_id"]
    spec_id = spec["metadata"]["spec_id"]

    milestone_dir = Path(f"milestones/{milestone_id}")
    milestone_dir.mkdir(parents=True, exist_ok=True)

    spec_file_path = milestone_dir / f"{spec_id}.md"

    # Generate specification content
    content = f"""{spec['frontmatter']}

# Specification {spec_id}

## Overview

**Specification ID:** {spec_id}
**Milestone:** {spec['metadata']['milestone_id']}
**Generated:** {spec['metadata']['generated_at']}

## Functional Requirements

"""

    for fr in spec['functional_requirements']:
        content += f"### {fr['semantic_id']}

{fr['text']}

"

    content += "\n## Interface Contracts\n\n"

    for contract in spec['interface_contracts']:
        content += f"- **{contract['type'].title()}**: {contract['description']}\n"

    content += "\n## Strict File Scope\n\n"
    content += "### Allowlist (Files permitted to change):")
    for file in spec['strict_file_scope']['allowlist']:
        content += f"\n- {file}"

    content += "\n\n### Denylist (Do NOT Touch):")
    for file in spec['strict_file_scope']['denylist']:
        content += f"\n- {file}"

    content += "\n\n## Affected Modules\n\n"
    for module in spec['affected_modules']:
        content += f"### {module['name']}\n\n"
        content += "**Public Interface:**\n"
        for export in module['exports']:
            content += f"- {export}\n"
        content += "\n"

    content += "\n## Implementation Tasks\n\n"
    for task in spec['implementation_tasks']:
        content += f"{task}\n"

    content += "\n## Next Steps\n\n"
    for step in spec['next_steps']:
        content += f"- {step}\n"

    content += f"\n---\n\n*This specification was auto-generated by the generate-spec skill*\n"

    spec_file_path.write_text(content)

    return str(spec_file_path)

def main() -> int:
    """Main skill execution function"""
    print("=== Generate Spec Skill ===")
    print("Version: 2.0.0-stable")
    print()

    # Show skill info
    skill_info = {
        "name": "generate-spec",
        "version": "2.0.0-stable",
        "description": "Transform an approved milestone document into a detailed implementation specification"
    }

    print(f"Skill Info: {skill_info}")
    print()

    # Check if M11 milestone exists
    milestone_content = read_milestone_file("M11")
    if not milestone_content:
        print("Error: M11 milestone not found in milestones/ directory")
        return 1

    print("M11 milestone found successfully")

    # Generate specifications for S1-S6
    specs_generated = []

    for spec_suffix in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']:
        spec_id = f"M11{spec_suffix}"
        print(f"\n--- Generating {spec_id} ---")

        spec = generate_specification("M11", spec_id)

        if "error" in spec:
            print(f"Error generating {spec_id}: {spec['error']}")
            continue

        # Write specification file
        spec_file_path = write_specification_file(spec)
        specs_generated.append(spec_file_path)

        print(f"Successfully generated: {spec_file_path}")
        print(f"  - FRs: {spec['metadata']['semantic_fr_count']}")
        print(f"  - Acceptance Criteria: {spec['metadata']['acceptance_criterion_count']}")

    print(f"\n=== Generation Complete ===")
    print(f"Specifications generated: {len(specs_generated)}")

    for spec_path in specs_generated:
        print(f"  - {spec_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
M12S1 Initial Failure Test - Behavioral-Vector Persona Overhaul

This test MUST FAIL initially because the current manage-development
SKILL.md does not implement the complete behavioral-vector persona
dover as specified in M12S1.

Validates all 6 behavioral-vector schema fields from FR-M12S1-1:
- baseline (>= 20 chars, present)
- pressure_shift (>= 20 chars, present)
- optimizes_for (>= 20 chars, present)
- neglects (>= 20 chars, present)
- phase_affinity (array, enum validation)
- continuation_anchor (boolean)

Also validates:
- All 7 personas present
- Correct persona IDs (pattern ^[a-z0-9-]+$)
- continuation_anchor: true only for the-implementer
- All other personas have continuation_anchor: false
- Valid phase_affinity enum values

Requirement: FR-M12S1-1, VR-M12S1-1, AC-M12S1-1
"""

import re
from pathlib import Path
from typing import Dict, Any, List

def extract_persona_vectors_from_skill():
    """Extract persona vectors from manage-development SKILL.md.

    Returns a dictionary of persona data with behavioral-vector fields.
    This parser correctly handles the actual format in SKILL.md:
    **Field:** Value (with colon and two asterisks)
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Pattern to match persona sections
    # Format: **Persona 1: the-skeptic** followed by field definitions
    persona_pattern = r'\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n---|\n\*\*Persona|\Z)'

    personas = {}

    for match in re.finditer(persona_pattern, content):
        persona_id = match.group(1)
        section = match.group(2)

        persona = {'id': persona_id}

        # Extract fields - note the actual format uses **Field:** (two asterisks)
        field_patterns = {
            'label': r'- \*\*Label:\s*([^\n]+)',  # Match any character except newline
            'baseline': r'- \*\*Baseline:\s*([^\n]+)',
            'pressure_shift': r'- \*\*Pressure Shift:\s*([^\n]+)',
            'optimizes_for': r'- \*\*Optimizes For:\s*([^\n]+)',
            'neglects': r'- \*\*Neglects:\s*([^\n]+)',
            'phase_affinity': r'- \*\*Phase Affinity:\s*([^\n]+)',
            'continuation_anchor': r'- \*\*Continuation Anchor:\s*([^\n]+)'
        }

        for field, pattern in field_patterns.items():
            field_match = re.search(pattern, section)
            if field_match:
                value = field_match.group(1).strip()

                if field == 'phase_affinity':
                    # Convert comma-separated list to array
                    persona[field] = [p.strip() for p in value.split(',')]
                elif field == 'continuation_anchor':
                    # Convert to boolean
                    persona[field] = value.lower() == 'true'
                else:
                    persona[field] = value

        personas[persona_id] = persona

    return personas

def test_behavioral_vector_schema_requirement():
    """Test FR-M12S1-1: Behavioral-Vector Persona Definition Schema.

    Each persona MUST be defined with four mandatory vector fields
    and two optional affinity fields.
    """
    personas = extract_persona_vectors_from_skill()

    # Test 1: All 7 personas must be present (FR-M12S1-2)
    expected_personas = {
        'the-skeptic', 'the-architect', 'the-implementer',
        'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst'
    }

    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas: {missing_personas}"

    extra_personas = set(personas.keys()) - expected_personas
    assert not extra_personas, f"Unexpected extra personas: {extra_personas}"

    # Test 2: Each persona must have all required behavioral-vector fields
    required_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects',
                      'phase_affinity', 'continuation_anchor']

    for persona_id, persona in personas.items():
        missing_fields = [field for field in required_fields if field not in persona]
        assert not missing_fields, \
            f"Persona '{persona_id}' missing behavioral-vector fields: {missing_fields}"

    print(f"✓ All {len(personas)} personas have complete behavioral-vector schema")

def test_field_content_requirements():
    """Test that all behavioral-vector fields meet content requirements."""
    personas = extract_persona_vectors_from_skill()

    # Test 1: All required string fields must be >= 20 characters
    required_string_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']

    for persona_id, persona in personas.items():
        for field in required_string_fields:
            value = persona.get(field, '')
            assert len(value.strip()) >= 20, \
                f"Persona '{persona_id}' field '{field}' too short "
                f"({len(value.strip())} chars, minimum 20)"

    print(f"✓ All {len(personas)} personas have string fields >= 20 chars")

    # Test 2: phase_affinity must be array with valid enum values
    valid_phases = ['milestone', 'specification', 'verification', 'tests', 'evaluation', 'implementation']

    for persona_id, persona in personas.items():
        phase_affinity = persona.get('phase_affinity', [])
        assert isinstance(phase_affinity, list), \
            f"Persona '{persona_id}' phase_affinity must be array, got {type(phase_affinity)}"

        for phase in phase_affinity:
            assert phase in valid_phases, \
                f"Persona '{persona_id}' phase_affinity contains invalid value: '{phase}'"

    print(f"✓ All {len(personas)} personas have valid phase_affinity enum values")

    # Test 3: continuation_anchor must be boolean
    for persona_id, persona in personas.items():
        anchor = persona.get('continuation_anchor')
        assert isinstance(anchor, bool), \
            f"Persona '{persona_id}' continuation_anchor must be boolean, got {type(anchor)}"

    # Test 4: Special requirement - the-implementer must have continuation_anchor: true
    implementer = personas.get('the-implementer')
    assert implementer is not None, "Persona 'the-implementer' not found"
    assert implementer['continuation_anchor'] == True, \
        "Persona 'the-implementer' must have continuation_anchor: true"

    # Test 5: All other personas must have continuation_anchor: false
    for persona_id, persona in personas.items():
        if persona_id != 'the-implementer':
            assert persona['continuation_anchor'] == False, \
                f"Persona '{persona_id}' (non-continuity anchor) must have continuation_anchor: false"

    print(f"✓ All {len(personas)} personas have correct continuation_anchor values")

    # Test 6: All persona IDs must match pattern ^[a-z0-9-]+$
    for persona_id in personas.keys():
        assert re.match(r'^[a-z0-9-]+$', persona_id), \
            f"Persona ID '{persona_id}' does not match pattern ^[a-z0-9-]+$"

    print(f"✓ All {len(personas)} persona IDs comply with required pattern")

if __name__ == "__main__":
    print("=" * 80)
    print("M12S1 Initial Failure Test Suite")
    print("=" * 80)
    print("\nThis test suite MUST FAIL initially.")
    print("The current manage-development SKILL.md does not implement")
    print("the complete behavioral-vector persona overhaul as specified in M12S1.")
    print("\nRequirement Coverage:")
    print("  FR-M12S1-1: Behavioral-Vector Persona Definition Schema")
    print("  VR-M12S1-1: Schema Validation")
    print("  AC-M12S1-1: Persona Vector Completeness")
    print("=" * 80 + "\n")

    try:
        test_behavioral_vector_schema_requirement()
        print()
        test_field_content_requirements()
        print()
        print("=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("\nThis indicates that the manage-development skill implementation")
        print("successfully implements the M12S1 behavioral-vector persona")
        print("overhaul as specified in the requirements.")
        print("\nThe TDD baseline has been met - tests now pass.")
        print("=" * 80 + "\n")

    except AssertionError as e:
        print("\n" + "=" * 80)
        print(f"❌ TEST FAILED: {e}")
        print("\nThis is the expected initial failure.")
        print("The tests confirm that the manage-development SKILL.md")
        print("does not yet have the complete behavioral-vector persona")
        print("definitions required by M12S1.")
        print("\nThe TDD baseline is valid - tests fail as expected.")
        print("=" * 80 + "\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

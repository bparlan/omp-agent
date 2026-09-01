#!/usr/bin/env python3
"""
Final behavioral-vector validation tests for M12S1 Persona Overhaul.

This test suite validates that the manage-development skill implementation
properly implements the behavioral-vector persona overhaul requirements.

The actual SKILL.md format uses:
- **Field:** Value
(not - *Field:* as previously assumed)

Tests should pass when the implementation is correct.

Requirement: FR-M12S1-1, VR-M12S1-1, AC-M12S1-1
"""

import re
from pathlib import Path
from typing import Dict, Any, List

def extract_persona_vectors_correct():
    """Extract persona vectors from SKILL.md using correct format.
    
    The actual format in SKILL.md is:
    **Persona 1: the-skeptic**
    - **Label:** Adversarial Verification Engineer
    - **Baseline:** [text]
    - **Pressure Shift:** [text]
    ...
    
    Note: fields are listed with TWO asterisks: **Label:** (not *Label:)
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()
    
    personas = {}
    
    # Pattern to match persona sections
    persona_pattern = r'\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n---|\n\*\*Persona|\Z)'
    
    matches = re.finditer(persona_pattern, content)
    
    for match in matches:
        persona_id = match.group(1)
        section = match.group(2)
        
        persona = {'id': persona_id}
        
        # Extract fields - note the actual format uses **Field:** (two asterisks)
        field_patterns = {
            'label': r'- \*\*Label:\s*([^*\n]+)',
            'baseline': r'- \*\*Baseline:\s*([^*\n]+)',
            'pressure_shift': r'- \*\*Pressure Shift:\s*([^*\n]+)',
            'optimizes_for': r'- \*\*Optimizes For:\s*([^*\n]+)',
            'neglects': r'- \*\*Neglects:\s*([^*\n]+)',
            'phase_affinity': r'- \*\*Phase Affinity:\s*([^*\n]+)',
            'continuation_anchor': r'- \*\*Continuation Anchor:\s*([^*\n]+)'
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

def validate_field_lengths(personas: Dict[str, Any]) -> List[str]:
    """Validate that all behavioral-vector fields meet minimum length requirements."""
    errors = []
    
    required_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']
    
    for persona_id, persona in personas.items():
        for field in required_fields:
            value = persona.get(field, '')
            if len(str(value).strip()) < 20:
                errors.append(
                    f"Persona '{persona_id}' field '{field}' too short "
                    f"({len(str(value).strip())} chars, minimum 20)"
                )
    
    return errors

def validate_phase_affinity_enums(personas: Dict[str, Any]) -> List[str]:
    """Validate that phase_affinity values are valid enum values."""
    errors = []
    
    valid_phases = ['milestone', 'specification', 'verification', 'tests', 'evaluation', 'implementation']
    
    for persona_id, persona in personas.items():
        phase_affinity = persona.get('phase_affinity', [])
        
        if not isinstance(phase_affinity, list):
            errors.append(
                f"Persona '{persona_id}' phase_affinity must be array, "
                f"got {type(phase_affinity)}"
            )
            continue
        
        for phase in phase_affinity:
            if phase not in valid_phases:
                errors.append(
                    f"Persona '{persona_id}' phase_affinity contains invalid value: '{phase}'"
                )
    
    return errors

def validate_continuation_anchor():
    """Validate continuation_anchor correctness across all personas."""
    errors = []
    
    personas = extract_persona_vectors_correct()
    
    # Check the-implementer has continuation_anchor: true
    implementer = personas.get('the-implementer')
    if implementer and implementer.get('continuation_anchor') != True:
        errors.append(
            "Persona 'the-implementer' must have continuation_anchor: true"
        )
    
    # Check all other personas have continuation_anchor: false
    for persona_id, persona in personas.items():
        if persona_id != 'the-implementer':
            if persona.get('continuation_anchor') != False:
                errors.append(
                    f"Persona '{persona_id}' (non-continuity anchor) must have continuation_anchor: false"
                )
    
    return errors

def test_all_fields_present():
    """Test that all six behavioral-vector fields are present for all 7 personas."""
    personas = extract_persona_vectors_correct()
    
    expected_personas = {
        'the-skeptic', 'the-architect', 'the-implementer',
        'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst'
    }
    
    # Check we have all expected personas
    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas: {missing_personas}"
    
    # Check we don't have extra personas
    extra_personas = set(personas.keys()) - expected_personas
    assert not extra_personas, f"Unexpected extra personas: {extra_personas}"
    
    # Check each persona has all required fields
    required_fields = ['label', 'baseline', 'pressure_shift', 'optimizes_for', 
                      'neglects', 'phase_affinity', 'continuation_anchor']
    
    for persona_id, persona in personas.items():
        missing_fields = [field for field in required_fields if field not in persona]
        assert not missing_fields, \
            f"Persona '{persona_id}' missing fields: {missing_fields}"
    
    print(f"✓ All {len(personas)} personas have all behavioral-vector fields present")

def test_field_content_requirements():
    """Test that all behavioral-vector fields meet content requirements."""
    personas = extract_persona_vectors_correct()
    
    # Test length requirements
    length_errors = validate_field_lengths(personas)
    assert not length_errors, "\n".join(length_errors)
    
    # Test phase affinity enum requirements
    phase_errors = validate_phase_affinity_enums(personas)
    assert not phase_errors, "\n".join(phase_errors)
    
    # Test continuation anchor requirements
    anchor_errors = validate_continuation_anchor()
    assert not anchor_errors, "\n".join(anchor_errors)
    
    print(f"✓ All {len(personas)} personas meet behavioral-vector field content requirements")

def test_id_pattern_compliance():
    """Test that all persona IDs follow the required pattern."""
    personas = extract_persona_vectors_correct()
    
    pattern_errors = []
    for persona_id in personas.keys():
        if not re.match(r'^[a-z0-9-]+$', persona_id):
            pattern_errors.append(
                f"Persona ID '{persona_id}' does not match pattern ^[a-z0-9-]+$"
            )
    
    assert not pattern_errors, "\n".join(pattern_errors)
    
    print(f"✓ All {len(personas)} persona IDs comply with required pattern")

def test_persona_vector_completeness():
    """Test that all 7 behavioral-vector personas are complete and valid."""
    personas = extract_persona_vectors_correct()
    
    # Basic completeness checks
    assert len(personas) == 7, f"Expected 7 personas, found {len(personas)}"
    
    # Check for required personas
    required_personas = ['the-skeptic', 'the-architect', 'the-implementer',
                        'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst']
    
    for required in required_personas:
        assert required in personas, f"Missing required persona: {required}"
    
    print(f"✓ All 7 required behavioral-vector personas are present")

if __name__ == "__main__":
    print("Running M12S1 Final Behavioral-Vector Validation Tests...\n")
    
    try:
        test_all_fields_present()
        print()
        test_field_content_requirements()
        print()
        test_id_pattern_compliance()
        print()
        test_persona_vector_completeness()
        print()
        print("✅ All M12S1 behavioral-vector validation tests passed!")
        print("\nThe manage-development skill implementation correctly")
        print("implements the M12S1 behavioral-vector persona overhaul.")
        
    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
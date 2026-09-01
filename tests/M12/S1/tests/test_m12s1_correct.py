#!/usr/bin/env python3
"""
Correct M12S1 test with proper regex for **Field:** format.

This test correctly parses the manage-development SKILL.md file,
which uses the format: - **Label:** Value (two asterisks)

The behavioral-vector persona overhaul M12S1 requires:
- All 7 personas present
- All 6 behavioral-vector fields per persona
- Field content meets requirements
- Correct field formats and values

This test will FAIL initially because the current SKILL.md
has incomplete behavioral-vector persona definitions.
"""

import re
from pathlib import Path
from typing import Dict, Any, List

def extract_persona_vectors_correct():
    """Extract persona vectors using CORRECT regex for **Field:** format.
    
    The actual SKILL.md format is:
    **Persona 1: the-skeptic**
    - **Label:** Adversarial Verification Engineer
    - **Baseline:** [text]
    - **Pressure Shift:** [text]
    ...
    
    Note: fields are listed with TWO asterisks: **Label:** (not *Label:)
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()
    
    # Pattern to match persona sections
    # Format: **Persona 1: the-skeptic** followed by fields
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

def validate_persona_completeness():
    """Test that all 7 behavioral-vector personas are complete."""
    personas = extract_persona_vectors_correct()
    
    # Expected 7 personas from FR-M12S1-2
    expected_personas = {
        'the-skeptic', 'the-architect', 'the-implementer',
        'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst'
    }
    
    # Requirement: All 7 personas MUST be present
    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas in SKILL.md: {missing_personas}"
    
    # Requirement: No extra personas
    extra_personas = set(personas.keys()) - expected_personas
    assert not extra_personas, f"Unexpected extra personas in SKILL.md: {extra_personas}"
    
    # Requirement: Each persona has all 6 behavioral-vector fields
    required_fields = ['label', 'baseline', 'pressure_shift', 'optimizes_for', 
                      'neglects', 'phase_affinity', 'continuation_anchor']
    
    for persona_id, persona in personas.items():
        missing_fields = [field for field in required_fields if field not in persona]
        assert not missing_fields, \
            f"Persona '{persona_id}' missing behavioral-vector fields: {missing_fields}"
    
    print(f"✓ All {len(personas)} personas have all 6 behavioral-vector fields")

def test_field_content_requirements():
    """Test that all behavioral-vector fields meet content requirements."""
    personas = extract_persona_vectors_correct()
    
    # Test 1: All string fields must be non-empty and >= 20 chars
    required_string_fields = ['label', 'baseline', 'pressure_shift', 'optimizes_for', 'neglects']
    
    for persona_id, persona in personas.items():
        for field in required_string_fields:
            value = persona.get(field, '')
            assert value and len(value.strip()) > 0, \
                f"Persona '{persona_id}' field '{field}' is empty"
            
            assert len(value.strip()) >= 20, \
                f"Persona '{persona_id}' field '{field}' too short ({len(value.strip())} chars, minimum 20)"
    
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

if __name__ == "__main____":
    print("Running M12S1 Correct Behavioral-Vector Persona Test...\n")
    print("This test validates the correct behavioral-vector persona")
    print("implementation as defined in M12S1.\n")
    
    try:
        validate_persona_completeness()
        print()
        test_field_content_requirements()
        print()
        print("✅ ALL TESTS PASSED!")
        print("\nThis indicates the manage-development skill implementation")
        print("successfully implements the M12S1 behavioral-vector")
        print("persona overhaul.\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("\nThis is the expected initial failure. The tests confirm that")
        print("the manage-development SKILL.md does not yet have the complete")
        print("behavioral-vector persona definitions required by M12S1.\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
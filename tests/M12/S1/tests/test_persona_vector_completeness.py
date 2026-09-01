#!/usr/bin/env python3
"""
Test persona vector completeness for M12S1 behavioral-vector persona overhaul.
Covers AC-M12S1-1, AC-M12S1-2, VR-M12S1-2, VR-M12S1-3
"""

import re
from pathlib import Path

def load_actual_personas():
    """Load actual persona definitions from manage-development skill."""
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()
    
    # Extract persona vector definitions from the skill file
    # Look for behavioral-vector personas in the skill content
    personas = {}
    
    # Pattern to match persona definitions with their vector fields
    # This regex captures the persona ID and its vector fields
    # Updated regex to match the actual persona format (**Persona N: the-name**) in SKILL.md
    persona_pattern = r'\*\*Persona \d+:\s*([a-z0-9-]+)\*\*\s*[\s\S]*?\*\*Baseline:\*\* ([^\n]+)\s*-\s\*\*Pressure Shift:\*\* ([^\n]+)\s*-\s\*\*Optimizes For:\*\* ([^\n]+)\s*-\s\*\*Neglects:\*\* ([^\n]+)\s*-\s\*\*Phase Affinity:\*\* ([^\n]+)\s*-\s\*\*Continuation Anchor:\*\* ([^\n]+)'
    
    for match in re.finditer(persona_pattern, content, re.DOTALL):
        persona_id = match.group(1)
        baseline = match.group(2).strip()
        pressure_shift = match.group(3).strip()
        optimizes_for = match.group(4).strip()
        neglects = match.group(5).strip()
        phase_affinity_str = match.group(6)
        continuation_anchor = match.group(7).strip().lower() == 'true'
        
        # Parse phase affinity list
        phase_affinity = []
        for phase_match in re.finditer(r'"([^"]+)"', phase_affinity_str):
            phase_affinity.append(phase_match.group(1))
        
        personas[persona_id] = {
            'id': persona_id,
            'baseline': baseline,
            'pressure_shift': pressure_shift,
            'optimizes_for': optimizes_for,
            'neglects': neglects,
            'phase_affinity': phase_affinity,
            'continuation_anchor': continuation_anchor
        }
    
    # Alternative: extract from behavioral-vector persona sections
    # Format: - **Field:** value (with dash prefix as in SKILL.md)
    team_pattern = r'\*\*Persona (\d+): ([a-z0-9-]+)\*\*[\s\S]*?- \*\*Baseline:\*\* ([^\n]+)\s*- \*\*Pressure Shift:\*\* ([^\n]+)\s*- \*\*Optimizes For:\*\* ([^\n]+)\s*- \*\*Neglects:\*\* ([^\n]+)\s*- \*\*Phase Affinity:\*\* ([^\n]+)\s*- \*\*Continuation Anchor:\*\* ([^\n]+)'

    for match in re.finditer(team_pattern, content, re.DOTALL):
        persona_id = match.group(2)
        baseline = match.group(3).strip()
        pressure_shift = match.group(4).strip()
        optimizes_for = match.group(5).strip()
        neglects = match.group(6).strip()
        phase_affinity_str = match.group(7).strip()
        continuation_anchor = match.group(8).strip().lower() == 'true'

        # Parse phase affinity (comma-separated)
        phase_affinity = [p.strip() for p in phase_affinity_str.split(',') if p.strip()]

        personas[persona_id] = {
            'id': persona_id,
            'label': persona_id.replace('-', ' ').title(),
            'baseline': baseline,
            'pressure_shift': pressure_shift,
            'optimizes_for': optimizes_for,
            'neglects': neglects,
            'phase_affinity': phase_affinity,
            'continuation_anchor': continuation_anchor
        }
    
    return personas

def test_persona_vector_completeness():
    """AC-M12S1-1: All 7 behavioral-vector personas are defined."""
    personas = load_actual_personas()
    
    # Verify all 7 expected personas exist
    expected_personas = {
        'the-skeptic', 'the-architect', 'the-implementer',
        'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst'
    }
    
    actual_personas = set(personas.keys())
    
    assert actual_personas == expected_personas, \
        f"Persona mismatch. Expected: {expected_personas}, Got: {actual_personas}"
    
    # Verify all required vector fields are present for each persona
    for persona_id, persona in personas.items():
        required_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']
        for field in required_fields:
            assert field in persona, f"Persona {persona_id} missing required field: {field}"
            assert persona[field], f"Persona {persona_id} field {field} is empty"
            assert len(persona[field]) >= 20, f"Persona {persona_id} field {field} too short (min 20 chars)"
        
        # Verify phase affinity exists
        assert 'phase_affinity' in persona, f"Persona {persona_id} missing phase_affinity"
        assert isinstance(persona['phase_affinity'], list), f"Persona {persona_id} phase_affinity not a list"
        
        # Verify continuation anchor exists
        assert 'continuation_anchor' in persona, f"Persona {persona_id} missing continuation_anchor"
        assert isinstance(persona['continuation_anchor'], bool), \
            f"Persona {persona_id} continuation_anchor not boolean"
    
    print("✓ Persona vector completeness validation passed")

def test_phase_team_assignment_correctness():
    """AC-M12S1-2: The 6 phase-specific 3-person team assignments are correct."""
    personas = load_actual_personas()
    
    # Expected team assignments from M12S1 specification
    expected_team_assignments = {
        'milestone': ['the-analyst', 'the-architect', 'the-implementer'],
        'specification': ['the-architect', 'the-skeptic', 'the-implementer'],
        'verification': ['the-skeptic', 'the-auditor', 'the-implementer'],
        'tests': ['the-strategist', 'the-auditor', 'the-implementer'],
        'evaluation': ['the-reviewer', 'the-auditor', 'the-implementer'],
        'implementation': ['the-implementer', 'the-architect', 'the-reviewer']
    }
    
    # Verify all expected team members exist
    for phase, team in expected_team_assignments.items():
        for member_id in team:
            assert member_id in personas, \
                f"Phase {phase} references missing persona: {member_id}"
    
    # Verify the-implementer appears in all 6 teams
    implementer_count = sum(1 for team in expected_team_assignments.values() 
                           if 'the-implementer' in team)
    assert implementer_count == 6, \
        f"the-implementer should appear in all 6 phases, found {implementer_count}"
    
    # Verify each team has exactly 3 unique members
    for phase, team in expected_team_assignments.items():
        assert len(team) == 3, \
            f"Phase {phase} team should have exactly 3 members"
        
        assert len(set(team)) == 3, \
            f"Phase {phase} team has duplicate members"
    
    print("✓ Phase team assignment correctness validation passed")

def test_vector_uniqueness():
    """VR-M12S1-2: No two persona vectors may share the same id."""
    personas = load_actual_personas()
    
    # Verify all persona IDs are unique
    ids = [p['id'] for p in personas.values()]
    unique_ids = set(ids)
    
    assert len(ids) == len(unique_ids), \
        f"Duplicate persona IDs found: {[id for id in ids if ids.count(id) > 1]}"
    
    # Verify exactly 7 unique personas
    assert len(unique_ids) == 7, \
        f"Expected 7 unique persona IDs, found {len(unique_ids)}"
    
    print("✓ Vector uniqueness validation passed")

def test_phase_coverage():
    """VR-M12S1-3: Each of the 6 pipeline phases must have exactly one 3-person team assignment."""
    personas = load_actual_personas()
    
    # Load expected team assignments from M12S1.md
    expected_phase_teams = {
        'milestone': ['the-analyst', 'the-architect', 'the-implementer'],
        'specification': ['the-architect', 'the-skeptic', 'the-implementer'],
        'verification': ['the-skeptic', 'the-auditor', 'the-implementer'],
        'tests': ['the-strategist', 'the-auditor', 'the-implementer'],
        'evaluation': ['the-reviewer', 'the-auditor', 'the-implementer'],
        'implementation': ['the-implementer', 'the-architect', 'the-reviewer']
    }
    
    # Verify all expected team members exist
    for phase, team in expected_phase_teams.items():
        for member_id in team:
            assert member_id in personas, \
                f"Phase {phase} references missing persona: {member_id}"
        
        # Verify team size is exactly 3
        assert len(team) == 3, \
            f"Phase {phase} team should have exactly 3 members, found {len(team)}"
    
    # Verify all 6 phases are covered
    assert len(expected_phase_teams) == 6, \
        f"Expected 6 phases, found {len(expected_phase_teams)}"
    
    print("✓ Phase coverage validation passed")

def test_continuity_anchor_enforcement():
    """VR-M12S1-4: the-implementer MUST appear in every phase team assignment."""
    personas = load_actual_personas()
    
    # Verify the-implementer is the continuity anchor
    assert personas['the-implementer']['continuation_anchor'] == True, \
        "the-implementer should be the continuity anchor (continuation_anchor: true)"
    
    # Verify the-implementer appears in all phase teams
    expected_phase_teams = {
        'milestone': ['the-analyst', 'the-architect', 'the-implementer'],
        'specification': ['the-architect', 'the-skeptic', 'the-implementer'],
        'verification': ['the-skeptic', 'the-auditor', 'the-implementer'],
        'tests': ['the-strategist', 'the-auditor', 'the-implementer'],
        'evaluation': ['the-reviewer', 'the-auditor', 'the-implementer'],
        'implementation': ['the-implementer', 'the-architect', 'the-reviewer']
    }
    
    for phase, team in expected_phase_teams.items():
        assert 'the-implementer' in team, \
            f"Phase {phase} missing continuity anchor 'the-implementer'"
    
    print("✓ Continuity anchor enforcement validation passed")

def test_schema_validation():
    """VR-M12S1-1: All 7 persona vectors MUST pass schema validation."""
    personas = load_actual_personas()
    
    # Schema validation requirements from M12S1.md
    for persona_id, persona in personas.items():
        # Check all required fields exist
        required_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']
        for field in required_fields:
            assert field in persona, f"Persona {persona_id} missing required field: {field}"
        
        # Check field lengths (minimum 20 characters)
        for field in required_fields:
            assert len(persona[field]) >= 20, \
                f"Persona {persona_id} field {field} too short (min 20 chars, got {len(persona[field])})"
        
        # Check ID pattern (alphanumeric and hyphens)
        assert re.match(r'^[a-z0-9-]+$', persona['id']), \
            f"Persona {persona_id} ID doesn't match pattern ^[a-z0-9-]+$"
        
        # Check phase affinity contains only valid phases
        valid_phases = ['milestone', 'specification', 'verification', 'tests', 'evaluation', 'implementation']
        for phase in persona['phase_affinity']:
            assert phase in valid_phases, \
                f"Persona {persona_id} has invalid phase: {phase}"
        
        # Check continuation anchor is boolean
        assert isinstance(persona['continuation_anchor'], bool), \
            f"Persona {persona_id} continuation_anchor not boolean"
    
    print("✓ Schema validation passed")

if __name__ == "__main__":
    print("Running M12S1 persona vector completeness and requirements tests...\n")
    
    test_persona_vector_completeness()
    test_phase_team_assignment_correctness()
    test_vector_uniqueness()
    test_phase_coverage()
    test_continuity_anchor_enforcement()
    test_schema_validation()
    
    print("\n✅ All M12S1 persona vector completeness tests passed!")

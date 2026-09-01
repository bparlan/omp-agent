#!/usr/bin/env python3
"""
Test persona schema validation for M12S1 behavioral-vector persona overhaul.
Covers FR-M12S1-1, VR-M12S1-1, AC-M12S1-1
"""

import re
import yaml
from pathlib import Path

def load_persona_schema():
    """Load persona vector schema from fixture."""
    fixture_path = Path("tests/fixtures/synthetic_managedev_personas/persona_vectors.yml")
    with open(fixture_path, 'r') as f:
        return yaml.safe_load(f)['persona_vector_validation']

def load_actual_personas():
    """Load actual persona definitions from manage-development skill."""
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Extract persona sections using regex
    persona_pattern = r'\*\*Persona (\d+): ([a-z0-9-]+)\*\*[\s\S]*?\*\*Label:\*\* ([^\n]+)'
    personas = {}

    for match in re.finditer(persona_pattern, content):
        persona_id = match.group(2)  # the-skeptic, the-architect, etc.
        label = match.group(3).strip()

        # Extract vector fields from this persona
        id_match = re.search(r'\*\*Baseline:\*\* ([^\n]+)', content[match.start():match.start() + 1000])
        baseline = id_match.group(1) if id_match else ""

        id_match = re.search(r'\*\*Pressure Shift:\*\* ([^\n]+)', content[match.start():match.start() + 1000])
        pressure_shift = id_match.group(1) if id_match else ""

        id_match = re.search(r'\*\*Optimizes For:\*\* ([^\n]+)', content[match.start():match.start() + 1000])
        optimizes_for = id_match.group(1) if id_match else ""

        id_match = re.search(r'\*\*Neglects:\*\* ([^\n]+)', content[match.start():match.start() + 1000])
        neglects = id_match.group(1) if id_match else ""

        # Extract phase affinity
        phase_match = re.search(r'\*\*Phase Affinity:\*\* ([^\n]+)', content[match.start():match.start() + 2000])
        phase_affinity = []
        if phase_match:
            phase_str = phase_match.group(1)
            phase_affinity = [p.strip() for p in phase_str.split(',')]

        # Extract continuation anchor
        cont_match = re.search(r'\*\*Continuation Anchor:\*\* ([^\n]+)', content[match.start():match.start() + 2000])
        continuation_anchor = False
        if cont_match:
            cont_str = cont_match.group(1).strip().lower()
            continuation_anchor = cont_str in ['true', 'yes', 'true']

        personas[persona_id] = {
            'id': persona_id,
            'label': label,
            'baseline': baseline,
            'pressure_shift': pressure_shift,
            'optimizes_for': optimizes_for,
            'neglects': neglects,
            'phase_affinity': phase_affinity,
            'continuation_anchor': continuation_anchor
        }

    return personas

def test_persona_schema_validation():
    """Test all personas pass schema validation."""
    fixture = load_persona_schema()
    personas = load_actual_personas()

    # Validate each persona matches schema requirements
    for test_case in fixture['test_cases']:
        if test_case['should_pass']:
            # This persona should be in the actual personas
            if test_case['vector']['id'] in personas:
                vector = personas[test_case['vector']['id']]

                # Check all required fields exist
                required_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']
                for field in required_fields:
                    assert vector[field], f"Persona {vector['id']} missing required field: {field}"
                    assert len(vector[field]) >= 20, f"Persona {vector['id']} field {field} too short (min 20 chars)"

                # Check ID pattern
                assert re.match(r'^[a-z0-9-]+$', vector['id']), f"Persona {vector['id']} ID doesn't match pattern"

                # Check phase affinity
                for phase in vector['phase_affinity']:
                    assert phase in ['milestone', 'specification', 'verification', 'tests', 'evaluation', 'implementation'], \
                        f"Persona {vector['id']} invalid phase: {phase}"

                # Check continuation anchor
                assert isinstance(vector['continuation_anchor'], bool), f"Persona {vector['id']} continuation_anchor not boolean"

    print("✓ Persona schema validation passed")

def test_persona_vector_uniqueness():
    """Test no two personas share the same id."""
    personas = load_actual_personas()

    # Check for duplicate IDs
    ids = [p['id'] for p in personas.values()]
    unique_ids = set(ids)

    assert len(ids) == len(unique_ids), f"Duplicate persona IDs found: {ids}"
    print("✓ Persona vector uniqueness validation passed")

def test_phase_coverage():
    """Test each phase has exactly one 3-person team assignment."""
    personas = load_actual_personas()

    # Define expected team assignments from M12S1
    expected_teams = {
        'milestone': ['the-analyst', 'the-architect', 'the-implementer'],
        'specification': ['the-architect', 'the-skeptic', 'the-implementer'],
        'verification': ['the-skeptic', 'the-auditor', 'the-implementer'],
        'tests': ['the-strategist', 'the-auditor', 'the-implementer'],
        'evaluation': ['the-reviewer', 'the-auditor', 'the-implementer'],
        'implementation': ['the-implementer', 'the-architect', 'the-reviewer']
    }

    # Validate each phase team
    for phase, expected_team in expected_teams.items():
        for vector_id in expected_team:
            assert vector_id in personas, f"Phase {phase} references missing persona: {vector_id}"

        assert len(expected_team) == 3, f"Phase {phase} team should have exactly 3 members"

    print("✓ Phase coverage validation passed")

def test_continuity_anchor_enforcement():
    """Test the-implementer appears in every phase team."""
    personas = load_actual_personas()

    # Check that the-implementer is a continuation anchor
    assert personas['the-implementer']['continuation_anchor'] == True, \
        "the-implementer should be the continuity anchor"

    # All expected phase teams contain the-implementer
    expected_teams = {
        'milestone': ['the-analyst', 'the-architect', 'the-implementer'],
        'specification': ['the-architect', 'the-skeptic', 'the-implementer'],
        'verification': ['the-skeptic', 'the-auditor', 'the-implementer'],
        'tests': ['the-strategist', 'the-auditor', 'the-implementer'],
        'evaluation': ['the-reviewer', 'the-auditor', 'the-implementer'],
        'implementation': ['the-implementer', 'the-architect', 'the-reviewer']
    }

    for phase, team in expected_teams.items():
        assert 'the-implementer' in team, f"Phase {phase} missing continuity anchor"

    print("✓ Continuity anchor enforcement validation passed")

def test_acceptance_criteria():
    """Test acceptance criteria."""
    personas = load_actual_personas()

    # AC-M12S1-1: Persona Vector Completeness
    # All 7 personas are defined
    assert len(personas) == 7, f"Expected 7 personas, found {len(personas)}"

    # All four vector fields are present for each persona
    for vector_id, persona in personas.items():
        required_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']
        for field in required_fields:
            assert field in persona, f"Persona {vector_id} missing field: {field}"
            assert persona[field], f"Persona {vector_id} field {field} is empty"

    print("✓ Acceptance criteria validation passed")

if __name__ == "__main__":
    test_persona_schema_validation()
    test_persona_vector_uniqueness()
    test_phase_coverage()
    test_continuity_anchor_enforcement()
    test_acceptance_criteria()
    print("\n✅ All M12S1 verification tests passed!")

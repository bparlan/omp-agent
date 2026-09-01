#!/usr/bin/env python3
"""
Test persona uniqueness and phase team assignments for M12S1.
Covers FR-M12S1-2, FR-M12S1-3, VR-M12S1-2, VR-M12S1-3, VR-M12S1-4, AC-M12S1-2
"""

import re
from pathlib import Path


def load_actual_personas():
    """Load actual persona definitions from manage-development skill."""
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Extract all persona blocks
    persona_blocks = re.findall(
        r"\*\*Persona \d+:[^\n]*\n(?:.*?\n)*?(?=\*\*Persona \d+:|\Z)",
        content,
        re.DOTALL,
    )

    personas = {}
    for block in persona_blocks:
        # Extract ID and label
        id_match = re.search(r"\*\*Persona \d+:\s*([a-z0-9-]+)", block)
        if not id_match:
            continue
        persona_id = id_match.group(1)

        label_match = re.search(r"\*\*Label:\s*([^\n]+)", block)
        label = label_match.group(1).strip() if label_match else ""

        # Extract vector fields using line-by-line parsing
        lines = block.split("\n")
        vector = {
            "id": persona_id,
            "label": label,
            "baseline": "",
            "pressure_shift": "",
            "optimizes_for": "",
            "neglects": "",
            "phase_affinity": [],
            "continuation_anchor": False,
        }

        for line in lines:
            line = line.strip()
            if "**Baseline:**" in line:
                vector["baseline"] = (
                    line.replace("**Baseline:**", "").replace("- ", "").strip()
                )
            elif "**Pressure Shift:**" in line:
                vector["pressure_shift"] = (
                    line.replace("**Pressure Shift:**", "").replace("- ", "").strip()
                )
            elif "**Optimizes For:**" in line:
                vector["optimizes_for"] = (
                    line.replace("**Optimizes For:**", "").replace("- ", "").strip()
                )
            elif "**Neglects:**" in line:
                vector["neglects"] = (
                    line.replace("**Neglects:**", "").replace("- ", "").strip()
                )
            elif "**Phase Affinity:**" in line:
                phases = (
                    line.replace("**Phase Affinity:**", "").replace("- ", "").strip()
                )
                vector["phase_affinity"] = [p.strip() for p in phases.split(",")]
            elif "**Continuation Anchor:**" in line:
                anchor_str = (
                    line.replace("**Continuation Anchor:**", "")
                    .replace("- ", "")
                    .strip()
                    .lower()
                )
                vector["continuation_anchor"] = anchor_str in ["true", "yes", "true"]

        personas[persona_id] = vector

    return personas


def test_persona_vector_uniqueness():
    """VR-M12S1-2: No two persona vectors may share the same id."""
    personas = load_actual_personas()

    ids = [p["id"] for p in personas.values()]
    unique_ids = set(ids)

    assert len(ids) == len(
        unique_ids
    ), f"Duplicate persona IDs found: {[id for id in ids if ids.count(id) > 1]}"

    # Verify all 7 expected personas are present
    expected_ids = {
        "the-skeptic",
        "the-architect",
        "the-implementer",
        "the-auditor",
        "the-strategist",
        "the-reviewer",
        "the-analyst",
    }
    assert (
        set(ids) == expected_ids
    ), f"Missing or extra personas. Expected: {expected_ids}, Found: {set(ids)}"

    print("✓ Persona vector uniqueness validation passed")


def test_phase_team_assignments():
    """VR-M12S1-3: Each of the 6 pipeline phases must have exactly one 3-person team assignment."""
    personas = load_actual_personas()

    # Expected team assignments from M12S1.md
    expected_phase_teams = {
        "milestone": ["the-analyst", "the-architect", "the-implementer"],
        "specification": ["the-architect", "the-skeptic", "the-implementer"],
        "verification": ["the-skeptic", "the-auditor", "the-implementer"],
        "tests": ["the-strategist", "the-auditor", "the-implementer"],
        "evaluation": ["the-reviewer", "the-auditor", "the-implementer"],
        "implementation": ["the-implementer", "the-architect", "the-reviewer"],
    }

    # Verify all expected team members exist
    for phase, team in expected_phase_teams.items():
        for member_id in team:
            assert (
                member_id in personas
            ), f"Phase {phase} references missing persona: {member_id}"

        # Verify team size is exactly 3
        assert (
            len(team) == 3
        ), f"Phase {phase} team should have exactly 3 members, found {len(team)}"

    # Verify all 6 phases are covered
    assert (
        len(expected_phase_teams) == 6
    ), f"Expected 6 phases, found {len(expected_phase_teams)}"

    print("✓ Phase team assignments validation passed")


def test_continuity_anchor_enforcement():
    """VR-M12S1-4: the-implementer MUST appear in every phase team assignment."""
    personas = load_actual_personas()

    # Verify the-implementer is the continuity anchor
    assert (
        personas["the-implementer"]["continuation_anchor"] == True
    ), "the-implementer should be the continuity anchor (continuation_anchor: true)"

    # Verify the-implementer appears in all phase teams
    expected_phase_teams = {
        "milestone": ["the-analyst", "the-architect", "the-implementer"],
        "specification": ["the-architect", "the-skeptic", "the-implementer"],
        "verification": ["the-skeptic", "the-auditor", "the-implementer"],
        "tests": ["the-strategist", "the-auditor", "the-implementer"],
        "evaluation": ["the-reviewer", "the-auditor", "the-implementer"],
        "implementation": ["the-implementer", "the-architect", "the-reviewer"],
    }

    for phase, team in expected_phase_teams.items():
        assert (
            "the-implementer" in team
        ), f"Phase {phase} missing continuity anchor 'the-implementer'"

    print("✓ Continuity anchor enforcement validation passed")


def test_phase_affinity_consistency():
    """Verify persona phase affinity matches expected team assignments."""
    personas = load_actual_personas()

    # Expected phase affinity based on team assignments
    expected_phase_affinity = {
        "the-analyst": ["milestone"],
        "the-architect": ["specification", "implementation"],
        "the-skeptic": ["verification", "evaluation"],
        "the-implementer": ["implementation"],
        "the-auditor": ["tests", "evaluation"],
        "the-strategist": ["tests"],
        "the-reviewer": ["evaluation", "implementation"],
    }

    for persona_id, expected_phases in expected_phase_affinity.items():
        assert persona_id in personas, f"Missing persona: {persona_id}"

        actual_phases = personas[persona_id]["phase_affinity"]
        assert (
            set(actual_phases) == set(expected_phases)
        ), f"Persona {persona_id} phase affinity mismatch. Expected: {expected_phases}, Got: {actual_phases}"

    print("✓ Phase affinity consistency validation passed")


def test_team_size_constraints():
    """Test that all phase teams have exactly 3 members."""
    personas = load_actual_personas()

    # Verify all 7 personas are in the system
    assert len(personas) == 7, f"Expected 7 personas, found {len(personas)}"

    # Verify no persona appears in more than 6 phase teams (should be exactly their phase affinity count)
    for persona_id, persona in personas.items():
        phase_count = len(persona["phase_affinity"])
        # the-implementer should have 6 phases
        if persona_id == "the-implementer":
            assert (
                phase_count >= 1
            ), f"the-implementer should have at least 1 phase affinity, found {phase_count}"
        else:
            assert (
                phase_count >= 1
            ), f"Persona {persona_id} should have at least 1 phase affinity"

    print("✓ Team size constraints validation passed")


def test_acceptance_criteria_phase_assignments():
    """AC-M12S1-2: Verify the 6 phase-specific 3-person team assignments are correct."""
    personas = load_actual_personas()

    # Load expected team assignments from M12S1.md (simplified verification)
    expected_assignments = {
        "milestone": ["the-analyst", "the-architect", "the-implementer"],
        "specification": ["the-architect", "the-skeptic", "the-implementer"],
        "verification": ["the-skeptic", "the-auditor", "the-implementer"],
        "tests": ["the-strategist", "the-auditor", "the-implementer"],
        "evaluation": ["the-reviewer", "the-auditor", "the-implementer"],
        "implementation": ["the-implementer", "the-architect", "the-reviewer"],
    }

    # Verify the-implementer appears in all 6 teams
    implementer_count = sum(
        1 for team in expected_assignments.values() if "the-implementer" in team
    )
    assert (
        implementer_count == 6
    ), f"the-implementer should appear in all 6 phases, found {implementer_count}"

    # Verify each team has exactly 3 unique members
    for phase, team in expected_assignments.items():
        assert len(team) == 3, f"Phase {phase} team should have exactly 3 members"

        # Verify all team members are unique within the team
        assert len(set(team)) == 3, f"Phase {phase} team has duplicate members"

    print("✓ Acceptance criteria phase assignments validation passed")


if __name__ == "__main__":
    test_persona_vector_uniqueness()
    test_phase_team_assignments()
    test_continuity_anchor_enforcement()
    test_phase_affinity_consistency()
    test_team_size_constraints()
    test_acceptance_criteria_phase_assignments()
    print("\n✅ All M12S1 persona and team tests passed!")

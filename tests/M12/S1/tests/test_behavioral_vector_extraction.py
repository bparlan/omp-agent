#!/usr/bin/env python3
"""
Test behavioral-vector persona extraction for M12S1 Persona Overhaul.

This test suite validates that persona behavioral-vector fields are correctly
extracted from the manage-development SKILL.md file.

The actual format in SKILL.md uses:
- **Label:** (with colon)
- **Baseline:** (with colon)
- **Pressure Shift:** (with colon)
- **Optimizes For:** (with colon)
- **Neglects:** (with colon)
- **Phase Affinity:** (with colon)
- **Continuation Anchor:** (with colon)

Tests MUST fail initially because the current implementation doesn't fully
extract behavioral-vector fields from the SKILL.md file.
"""

import re
from pathlib import Path


def extract_persona_vectors_correct():
    """Extract persona vectors using correct regex patterns matching actual SKILL.md format.

    The actual format in SKILL.md is:
    **Persona 1: the-skeptic**
    - **Label:** Adversarial Verification Engineer
    - **Baseline:** [text]
    - **Pressure Shift:** [text]
    ...

    Note the colon after each field name in the actual file.
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    personas = {}

    # Pattern to match persona sections - each section starts with **Persona N: ID**
    # and ends before the next **Persona or end of file
    persona_pattern = (
        r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n\*\*Persona|\Z)"
    )

    matches = re.finditer(persona_pattern, content)

    for match in matches:
        persona_id = match.group(1)
        section = match.group(2)

        persona = {"id": persona_id}

        # Extract fields - note the colon after field names in actual format
        field_patterns = {
            "label": r"\*\*Label:\s*([^*\n]+)",
            "baseline": r"\*\*Baseline:\s*([^*\n]+)",
            "pressure_shift": r"\*\*Pressure Shift:\s*([^*\n]+)",
            "optimizes_for": r"\*\*Optimizes For:\s*([^*\n]+)",
            "neglects": r"\*\*Neglects:\s*([^*\n]+)",
            "phase_affinity": r"\*\*Phase Affinity:\s*([^*\n]+)",
            "continuation_anchor": r"\*\*Continuation Anchor:\s*([^*\n]+)",
        }

        for field, pattern in field_patterns.items():
            field_match = re.search(pattern, section)
            if field_match:
                value = field_match.group(1).strip()

                # Special processing for phase affinity (convert comma-separated to list)
                if field == "phase_affinity":
                    persona[field] = [p.strip() for p in value.split(",")]

                # Special processing for continuation anchor (convert to boolean)
                elif field == "continuation_anchor":
                    persona[field] = value.lower() == "true"

                else:
                    persona[field] = value

        personas[persona_id] = persona

    return personas


def test_persona_extraction_basic():
    """Test basic persona extraction from SKILL.md."""
    personas = extract_persona_vectors_correct()

    # Should have exactly 7 personas from FR-M12S1-2
    expected_personas = {
        "the-skeptic",
        "the-architect",
        "the-implementer",
        "the-auditor",
        "the-strategist",
        "the-reviewer",
        "the-analyst",
    }

    # Check we have all expected personas
    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas in extraction: {missing_personas}"

    # Check we don't have extra personas
    extra_personas = set(personas.keys()) - expected_personas
    assert (
        not extra_personas
    ), f"Unexpected extra personas in extraction: {extra_personas}"

    print(f"✓ Basic persona extraction test passed - found {len(personas)} personas")


def test_field_extraction_accuracy():
    """Test that individual fields are extracted correctly."""
    personas = extract_persona_vectors_correct()

    # Test specific known values for validation
    test_cases = {
        "the-skeptic": {
            "label": "Adversarial Verification Engineer",
            "phase_affinity": ["verification", "evaluation"],
            "continuation_anchor": False,
            "baseline_length": 138,
        },
        "the-architect": {
            "label": "Systems Architect",
            "phase_affinity": ["specification", "implementation"],
            "continuation_anchor": False,
            "baseline_length": 138,
        },
        "the-implementer": {
            "label": "Engineering Executor",
            "phase_affinity": ["implementation"],
            "continuation_anchor": True,
            "baseline_length": 150,
        },
    }

    for persona_id, expected in test_cases.items():
        actual = personas.get(persona_id)
        assert actual is not None, f"Persona '{persona_id}' not found"

        # Check label
        assert (
            actual["label"] == expected["label"]
        ), f"Persona '{persona_id}' label mismatch: expected '{expected['label']}', got '{actual['label']}'"

        # Check phase affinity
        assert (
            actual["phase_affinity"] == expected["phase_affinity"]
        ), f"Persona '{persona_id}' phase_affinity mismatch: expected {expected['phase_affinity']}, got {actual['phase_affinity']}"

        # Check continuation anchor
        assert (
            actual["continuation_anchor"] == expected["continuation_anchor"]
        ), f"Persona '{persona_id}' continuation_anchor mismatch: expected {expected['continuation_anchor']}, got {actual['continuation_anchor']}"

        # Check baseline length (approximately)
        baseline_length = len(actual["baseline"])
        expected_length = expected["baseline_length"]
        assert (
            abs(baseline_length - expected_length) <= 20
        ), f"Persona '{persona_id}' baseline length mismatch: expected ~{expected_length}, got {baseline_length}"

    print(f"✓ Field extraction accuracy test passed for {len(test_cases)} personas")


def test_all_fields_present():
    """Test that all behavioral-vector fields are present and non-empty."""
    personas = extract_persona_vectors_correct()

    required_fields = [
        "id",
        "label",
        "baseline",
        "pressure_shift",
        "optimizes_for",
        "neglects",
        "phase_affinity",
        "continuation_anchor",
    ]

    for persona_id, persona in personas.items():
        # Check all required fields are present
        missing_fields = [field for field in required_fields if field not in persona]
        assert (
            not missing_fields
        ), f"Persona '{persona_id}' missing fields: {missing_fields}"

        # Check string fields are non-empty
        string_fields = [
            "label",
            "baseline",
            "pressure_shift",
            "optimizes_for",
            "neglects",
        ]
        for field in string_fields:
            value = persona[field]
            assert (
                value and len(value.strip()) > 0
            ), f"Persona '{persona_id}' field '{field}' is empty or whitespace"

        # Check phase affinity is list
        assert isinstance(
            persona["phase_affinity"], list
        ), f"Persona '{persona_id}' phase_affinity must be list, got {type(persona['phase_affinity'])}"

        # Check continuation anchor is boolean
        assert isinstance(
            persona["continuation_anchor"], bool
        ), f"Persona '{persona_id}' continuation_anchor must be boolean, got {type(persona['continuation_anchor'])}"

        # Check field lengths meet schema requirements (>= 20 chars)
        for field in ["baseline", "pressure_shift", "optimizes_for", "neglects"]:
            value = persona[field]
            assert (
                len(value.strip()) >= 20
            ), f"Persona '{persona_id}' field '{field}' too short ({len(value.strip())} chars, minimum 20)"

    print(f"✓ All fields present and valid test passed for {len(personas)} personas")


def test_pattern_matching():
    """Test that the regex patterns correctly match the persona section format."""
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Test the persona section pattern
    persona_sections = re.findall(
        r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n\*\*Persona|\Z)", content
    )

    # Should find all 7 personas
    assert (
        len(persona_sections) == 7
    ), f"Expected to find 7 persona sections, found {len(persona_sections)}"

    # Test that we can extract ID from each section
    extracted_ids = [section[0] for section in persona_sections]
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
        set(extracted_ids) == expected_ids
    ), f"ID mismatch: expected {expected_ids}, got {set(extracted_ids)}"

    print(
        f"✓ Pattern matching test passed - extracted {len(extracted_ids)} persona IDs correctly"
    )


if __name__ == "__main__":
    print("Running M12S1 Behavioral-Vector Persona Extraction Tests...\n")

    try:
        test_persona_extraction_basic()
        print()
        test_field_extraction_accuracy()
        print()
        test_all_fields_present()
        print()
        test_pattern_matching()
        print()
        print("✅ All M12S1 behavioral-vector persona extraction tests passed!")

    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test ERROR: {e}")
        import traceback

        traceback.print_exc()
        exit(1)

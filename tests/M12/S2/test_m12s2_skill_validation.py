#!/usr/bin/env python3
# Verification IDs: VI-M12S2-1, VI-M12S2-6
# Requirement IDs: FR-M12S2-MANAGE_DOCS_SKILL_CREATION, FR-M12S2-OPERATIONS_PERSONAS
# Test Type: SPECIFICATION_CHECK

import sys
from pathlib import Path

REPO_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / "AGENTS.md").exists() or (p / ".git").exists()
    ),
    Path(__file__).resolve().parents[4],
)
SPEC_PATH = REPO_ROOT / "skills" / "manage-docs" / "SKILL.md"
PERSONA_SCHEMA_REQUIRED = [
    "id",
    "baseline",
    "pressure_shift",
    "optimizes_for",
    "neglects",
    "phase_affinity",
    "continuation_anchor",
]
MIN_LENGTHS = {
    "id": 1,
    "baseline": 20,
    "pressure_shift": 20,
    "optimizes_for": 20,
    "neglects": 20,
    "phase_affinity": 1,
    "continuation_anchor": 20,
}


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_(msg):
    print(f"PASS: {msg}")


def extract_table_personas(text):
    personas = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if "| ID | Baseline" in stripped and "Pressure Shift" in stripped:
            in_table = True
            continue
        if in_table:
            if not stripped.startswith("|"):
                break
            if stripped.startswith("|---"):
                continue
            parts = [part.strip() for part in stripped.split("|")[1:-1]]
            if len(parts) >= 7 and parts[0] != ":---":
                personas.append(
                    {
                        "id": parts[0].strip("`"),
                        "baseline": parts[1],
                        "pressure_shift": parts[2],
                        "optimizes_for": parts[3],
                        "neglects": parts[4],
                        "phase_affinity": parts[5],
                        "continuation_anchor": parts[6],
                    }
                )
    return personas


def main():
    if not SPEC_PATH.exists():
        fail(f"{SPEC_PATH}: file does not exist")

    personas = extract_table_personas(SPEC_PATH.read_text())
    if len(personas) != 7:
        fail(f"Expected 7 personas, found {len(personas)}")

    ids = []
    for p in personas:
        for key in PERSONA_SCHEMA_REQUIRED:
            value = p.get(key)
            min_len = MIN_LENGTHS.get(key, 20)
            if not isinstance(value, str) or len(value) < min_len:
                fail(f"Persona {p.get('id')}: field {key} is too short or missing")
        ids.append(p["id"])

    if len(set(ids)) != 7:
        fail(f"Duplicate persona ids: {ids}")

    pass_("Manage-docs skill file validation passed")


if __name__ == "__main__":
    main()

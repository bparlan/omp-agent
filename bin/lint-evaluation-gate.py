#!/usr/bin/env python3
"""
lint-evaluation-gate.py — Evidence-Floor & Self-Contradiction Gate

Mechanical (regex/structural) lint check for evaluation (*E.md) and completion
(*C.md) reports. Two independent checks:

  CHECK 1 — EVIDENCE_GAP:
    Summary counters (TESTS_RUN=N, EXIT_CODE=N, etc.) are present but zero
    raw evidence blocks are populated. This is the "M18S3E.md six-line shape"
    pattern: claim without trace.

  CHECK 2 — SELF-CONTRADICTION:
    Resolution-language (COMPLETE, Exit Code: 0, RESOLVED) co-occurs with
    pending-language (BLOCKED, PENDING, TEST_VALIDATION_BLOCKED) in the same
    document without an explicit qualifying-scope statement.

Usage:
  ./bin/lint-evaluation-gate.py milestones/M{X}/M{X}S{Y}E.md
  ./bin/lint-evaluation-gate.py milestones/M{X}/M{X}S{Y}C.md
  ./bin/lint-evaluation-gate.py docs/remediation/example_M18S1E_structured_block.md

Exit codes:
  0 — all checks pass
  1 — at least one check flag raised
  2 — file not found or unreadable
"""

import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# CHECK 1 — EVIDENCE_GAP
# ---------------------------------------------------------------------------

# Patterns that identify "counter-only" reports (claims without traces)
COUNTER_PATTERNS: list[re.Pattern] = [
    re.compile(r"^TESTS_RUN\s*=\s*\d+", re.MULTILINE),
    re.compile(r"^TESTS_PASSED\s*=\s*\d+", re.MULTILINE),
    re.compile(r"^TESTS_FAILED\s*=\s*\d+", re.MULTILINE),
    re.compile(r"^VALID_TESTS\s*=\s*\d+", re.MULTILINE),
    re.compile(r"^INVALID_TESTS\s*=\s*\d+", re.MULTILINE),
    re.compile(r"^EXIT_CODE\s*=\s*\d+", re.MULTILINE),
]

# Patterns that indicate raw evidence IS present (populated blocks)
EVIDENCE_PATTERNS: list[re.Pattern] = [
    # Populated YAML raw_evidence field (non-empty: has content after | or text)
    re.compile(r"raw_evidence:\s*\|?\s*\S"),
    # Populated fenced evidence block with a command
    re.compile(r"\$ ", re.MULTILINE),
    # Populated "checklist" evidence row
    re.compile(r"-\s*\[[xX]\]\s+.+?:?\s*`[^`]+`\s*→"),
    # Literal "[claim:" marker (evidence block header)
    re.compile(r"\[claim:\s*\S"),
    # Manual check with a reason populated
    re.compile(r"Check type:\s*MANUAL"),
    # Non-empty stdout/stderr capture
    re.compile(r"^stdout:\s*\S", re.MULTILINE),
    re.compile(r"^stderr:\s*\S", re.MULTILINE),
]


def check_evidence_gap(text: str, path: str) -> list[str]:
    """
    Return a list of flag messages, one per counter group found without evidence.
    Empty list = pass.
    """
    has_counters = any(p.search(text) for p in COUNTER_PATTERNS)
    if not has_counters:
        return []  # Not a counter-style report; skip

    has_evidence = any(p.search(text) for p in EVIDENCE_PATTERNS)
    if has_evidence:
        return []  # Evidence is present; pass

    # Count which counter patterns matched
    matched_counters = []
    for p in COUNTER_PATTERNS:
        m = p.search(text)
        if m:
            matched_counters.append(m.group().strip())

    return [
        f"EVIDENCE_GAP: {path} has summary counters ({'; '.join(matched_counters)}) "
        "but zero populated raw evidence blocks. Every counter claim must have "
        "a corresponding command trace or manual-check justification."
    ]


# ---------------------------------------------------------------------------
# CHECK 2 — SELF-CONTRADICTION
# ---------------------------------------------------------------------------

# Resolution-language markers (strong claims of completeness)
RESOLUTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"✅\s*COMPLETE"),
    re.compile(r"Exit Code:\s*0\b"),
    re.compile(r"No blocking issues remain", re.IGNORECASE),
    re.compile(r"All tests passed", re.IGNORECASE),
    re.compile(r"all critical defects resolved", re.IGNORECASE),
    re.compile(r"\bRESOLVED\b"),
    re.compile(r"✔️\s*COMPLETE"),
    re.compile(r"✅\s*FIXED"),
    re.compile(r"✅\s*RESOLVED"),
]

# Pending-language markers (claims of incompleteness or blockers)
PENDING_PATTERNS: list[re.Pattern] = [
    re.compile(r"⚠️\s*PENDING"),
    re.compile(r"⚠️\s*BLOCKED"),
    re.compile(r"\bBLOCKED\b"),
    re.compile(r"\bTEST_VALIDATION_BLOCKED\b"),
    re.compile(r"\bPENDING\b"),
    re.compile(r"❌\s*BLOCKED"),
]

# Qualifying scope statements that disambiguate resolution + pending co-occurrence
QUALIFIER_PATTERNS: list[re.Pattern] = [
    re.compile(r"(?i)scope\s*:"),
    re.compile(r"(?i)applies\s+to\b"),
    re.compile(r"(?i)applies\s+only\s+to\b"),
    re.compile(r"\bsubset\s*:"),
    re.compile(r"\bpartial\s*:"),
    re.compile(r"Only applicable to", re.IGNORECASE),
    re.compile(r"This (exit code|status|result) applies", re.IGNORECASE),
    re.compile(
        r"Exit Code:\s*\d+\s+\(", re.IGNORECASE
    ),  # qualified codes like "Exit Code: 0 (PASS)" vs bare
]


def check_self_contradiction(text: str, path: str) -> list[str]:
    """
    Return a list of flag messages for contradictory resolution + pending language.
    Empty list = pass.
    """
    # Find ALL resolution matches with their matched text and line context
    resolution_matches = []
    for p in RESOLUTION_PATTERNS:
        for m in p.finditer(text):
            resolution_matches.append(m.group().strip())

    # Find ALL pending matches
    pending_matches = []
    for p in PENDING_PATTERNS:
        for m in p.finditer(text):
            pending_matches.append(m.group().strip())

    # If either set is empty, no contradiction possible
    if not resolution_matches or not pending_matches:
        return []

    # Check for qualifying scope statement
    has_qualifier = any(p.search(text) for p in QUALIFIER_PATTERNS)

    if has_qualifier:
        return []  # Scope qualifier disambiguates

    # Deduplicate
    resolution_unique = sorted(set(resolution_matches))
    pending_unique = sorted(set(pending_matches))

    return [
        f"SELF_CONTRADICTION: {path} has resolution language "
        f"({'; '.join(resolution_unique)}) co-occurring with pending language "
        f"({'; '.join(pending_unique)}) but no qualifying scope statement "
        "that disambiguates which parts are complete vs pending. "
        "Add a scope: qualifier (e.g., 'scope: schema checks only') "
        "or resolve the contradiction by updating one of the conflicting claims."
    ]


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------


def lint_file(file_path: str) -> int:
    """Lint a single evaluation or completion report. Returns 0 = pass, 1 = fail."""
    path = Path(file_path)

    if not path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return 2

    if not path.is_file():
        print(f"ERROR: Not a file: {file_path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")

    findings: list[str] = []

    # Check 1: Evidence gap
    findings.extend(check_evidence_gap(text, file_path))

    # Check 2: Self-contradiction
    findings.extend(check_self_contradiction(text, file_path))

    if not findings:
        return 0

    for f in findings:
        print(f)

    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print(
            f"Usage: {sys.argv[0]} <evaluation_or_completion_file> [...]",
            file=sys.stderr,
        )
        print("", file=sys.stderr)
        print(
            "Lint one or more evaluation (*E.md) or completion (*C.md) reports.",
            file=sys.stderr,
        )
        print(
            "Exit code 0 = pass, 1 = findings raised, 2 = file error.", file=sys.stderr
        )
        return 2

    exit_code = 0
    for arg in sys.argv[1:]:
        result = lint_file(arg)
        if result != 0:
            exit_code = result

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

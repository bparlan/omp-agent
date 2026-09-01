#!/bin/bash
# test_m12s1t1_07_skills_ledger.sh - Skills ledger consistency validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-07: Skills Ledger Consistency"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="VR-M12S1-7"

# Load fixture
FIXTURE_FILE="../../../tests/fixtures/synthetic_managedev_personas/skills_ledger_expected.json"

if [[ ! -f "$FIXTURE_FILE" ]]; then
    echo "FAIL: Test fixture not found: $FIXTURE_FILE"
    exit 1
fi

echo "========================================================"
echo "Running: $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "========================================================"

# Verify skills-ledger.json is valid JSON
LEDGER_FILE="skills-ledger.json"
if [[ ! -f "$LEDGER_FILE" ]]; then
    echo "FAIL: skills-ledger.json not found"
    exit 1
fi

if ! python3 -c "import json; json.load(open('$LEDGER_FILE'))" 2>/dev/null; then
    echo "FAIL: skills-ledger.json is not valid JSON"
    exit 1
fi

echo "PASS: skills-ledger.json is valid JSON"

# Verify manage-development entry exists and contains persona metadata
python3 -c "
import json
import sys

with open('$LEDGER_FILE') as f:
    ledger = json.load(f)

# Check manage-development entry exists
if 'manage-development' not in ledger:
    print('FAIL: manage-development entry missing from skills-ledger.json')
    sys.exit(1)

print('PASS: manage-development entry exists in skills-ledger.json')

# Check personas array exists
if 'personas' not in ledger['manage-development']:
    print('FAIL: personas array missing from manage-development entry')
    sys.exit(1)

print('PASS: personas array exists in manage-development entry')

# Check exactly 7 personas
personas = ledger['manage-development']['personas']
if not isinstance(personas, list):
    print('FAIL: personas is not a list')
    sys.exit(1)

if len(personas) != 7:
    print(f'FAIL: Expected 7 personas, found {len(personas)}')
    sys.exit(1)

print(f'PASS: personas array contains exactly 7 entries')

# Check all required vector IDs are present
required_ids = ['the-skeptic', 'the-architect', 'the-implementer', 'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst']
found_ids = [p.get('id') for p in personas if isinstance(p, dict)]

for req_id in required_ids:
    if req_id not in found_ids:
        print(f'FAIL: Required persona id missing: {req_id}')
        sys.exit(1)

print('PASS: All 7 required persona vector IDs are present')

# Check no duplicate IDs
if len(found_ids) != len(set(found_ids)):
    print('FAIL: Duplicate persona IDs detected')
    sys.exit(1)

print('PASS: All persona IDs are unique')

# Verify against expected fixture structure
with open('$FIXTURE_FILE') as f:
    expected = json.load(f)

# Check schema matches
if ledger['manage-development']['schema'] != expected['schema']:
    print(f'FAIL: Schema mismatch: {ledger[\"manage-development\"][\"schema\"]} vs {expected[\"schema\"]}')
    sys.exit(1)

print('PASS: skills-ledger.json schema matches expected fixture')

# Verify phase_team_assignments structure
ledger_phases = ledger['manage-development'].get('phase_team_assignments', {})
expected_phases = expected.get('phase_team_assignments', {})

if len(ledger_phases) != len(expected_phases):
    print(f'FAIL: Phase team assignments count mismatch: {len(ledger_phases)} vs {len(expected_phases)}')
    sys.exit(1)

print('PASS: Phase team assignments count matches expected fixture')

# Verify each phase has exactly 3 members
for phase in expected_phases:
    if phase not in ledger_phases:
        print(f'FAIL: Phase {phase} missing from ledger')
        sys.exit(1)
    
    ledger_team = ledger_phases[phase]
    expected_team = expected_phases[phase]
    
    if len(ledger_team) != len(expected_team):
        print(f'FAIL: Phase {phase} team size mismatch: {len(ledger_team)} vs {len(expected_team)}')
        sys.exit(1)
    
    # Check members are in the correct order
    if ledger_team != expected_team:
        print(f'FAIL: Phase {phase} team members mismatch: {ledger_team} vs {expected_team}')
        sys.exit(1)

print('PASS: All phase team assignments match expected fixture')
print('SUCCESS: skills-ledger.json passes all consistency checks')
"

echo ""
echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Tests Run: 5"
echo "Tests Passed: 5"
echo "Tests Failed: 0"
echo "Expected Results: Skills ledger consistency checks pass (EXIT_CODE=0)"
echo "========================================================"

exit 0

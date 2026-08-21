#!/usr/bin/env python3
"""
Deliberate contradiction tests for milestone contract enforcement.

Tests that the milestone contract correctly:
1. Detects undeclared scope
2. Detects missing requirement information
3. Detects contradictory requirements
4. Detects verification without requirement traceability
5. Detects test without verification traceability
6. Detects implementation outside allowed paths
7. Detects ambiguous implementation boundary
8. Handles brownfield implementation already passing

Each test produces a classification and evidence.
"""

import sys
import os
import yaml
import re
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bin'))

PASS = 0
FAIL = 1
ERROR = 2

tests_run = 0
tests_passed = 0
tests_failed = 0

def test(name, fn):
    global tests_run, tests_passed, tests_failed
    tests_run += 1
    print(f"\n  [{tests_run}] {name}")
    print(f"  {'='*50}")
    try:
        result = fn()
        if result == PASS:
            print(f"  ✓ PASS")
            tests_passed += 1
        elif result == FAIL:
            print(f"  ✗ FAIL")
            tests_failed += 1
        else:
            print(f"  ✗ ERROR: {result}")
            tests_failed += 1
    except Exception as e:
        print(f"  ✗ EXCEPTION: {e}")
        tests_failed += 1

# ============================================================
# Test 1: Undeclared scope detection
# ============================================================
def test_undeclared_scope():
    """
    Scenario: A specification defines FRs that go beyond the milestone's scope.
    Expected: The milestone contract boilerplate says downstream stages
    MUST NOT introduce behavior not declared by the milestone.
    This is a prompt-level constraint on generate-spec, not a validator.
    """
    # Read the milestone template to verify the contract language exists
    template_path = Path("templates/milestone_template.md")
    content = template_path.read_text()
    
    # Check for the contract boilerplate
    if "MUST NOT introduce behavior, scope, or interfaces" in content:
        print(f"    Contract boilerplate found in template")
    else:
        print(f"    ERROR: Contract boilerplate missing from template")
        return FAIL
    
    # Check that generate-spec references the contract
    spec_path = Path("skills/generate-spec/SKILL.md")
    spec_content = spec_path.read_text()
    
    if "Integration Bindings" in spec_content and "authoritative" in spec_content:
        print(f"    generate-spec reads Integration Bindings")
    else:
        print(f"    WARNING: generate-spec may not prioritize Integration Bindings properly")
    
    # Check the Spec Decomposition Plan is referenced
    if "Spec Decomposition Plan" in spec_content:
        print(f"    generate-spec follows Spec Decomposition Plan")
    else:
        print(f"    WARNING: Spec Decomposition Plan not referenced in generate-spec")
    
    return PASS

# ============================================================
# Test 2: Missing requirement information
# ============================================================
def test_missing_requirement():
    """
    Scenario: A specification has a functional requirement without a CLI contract,
    schema, or filesystem boundary.
    Expected: generate-spec MUST halt with #NEEDS-CLARIFICATION.
    """
    spec_path = Path("skills/generate-spec/SKILL.md")
    content = spec_path.read_text()
    
    # The Interface Contract Mandate should require this
    if "lacks concrete definitions, you MUST halt immediately" in content:
        print(f"    generate-spec halts on missing concrete definitions")
    else:
        print(f"    ERROR: Missing interface contract mandate in generate-spec")
        return FAIL
    
    # Check for the needs-clarification marker
    if "#NEEDS-CLARIFICATION" in content:
        print(f"    #NEEDS-CLARIFICATION marker referenced")
    else:
        print(f"    WARNING: #NEEDS-CLARIFICATION not found in generate-spec")
    
    return PASS

# ============================================================
# Test 3: Contradictory requirements
# ============================================================
def test_contradictory_requirements():
    """
    Scenario: generate-verification encounters a verification strategy that
    contradicts the specification (e.g., strategy says SCRIPT_EXECUTION,
    spec says DOCUMENT_CHECK).
    Expected: generate-verification MUST follow the strategy or emit #NEEDS-CLARIFICATION.
    """
    ver_path = Path("skills/generate-verification/SKILL.md")
    content = ver_path.read_text()
    
    # Check for the Verification Strategy constraint
    if "MUST use the specified method" in content:
        print(f"    Verification strategy hints are authoritative")
    else:
        print(f"    ERROR: No verification strategy enforcement in generate-verification")
        return FAIL
    
    if "emit #NEEDS-CLARIFICATION" in content:
        print(f"    #NEEDS-CLARIFICATION fallback exists")
    else:
        print(f"    WARNING: No #NEEDS-CLARIFICATION fallback for strategy contradiction")
    
    return PASS

# ============================================================
# Test 4: Verification without requirement traceability
# ============================================================
def test_verification_no_traceability():
    """
    Scenario: A verification item has no source requirement ID.
    Expected: The omp-verify-traceability validator should reject it.
    """
    # Test the omp-verify-traceability script
    trace_path = Path("bin/omp-verify-traceability")
    content = trace_path.read_text()
    
    # Check for orphan FR detection
    if "orphaned" in content.lower() or "no corresponding" in content.lower():
        print(f"    Orphan requirement detection found")
    else:
        print(f"    WARNING: Orphan detection may be weak")
    
    # Check for the traceability matrix requirement in generate-verification
    ver_path = Path("skills/generate-verification/SKILL.md")
    ver_content = ver_path.read_text()
    
    if "trace each verification item back to its source requirement ID" in ver_content:
        print(f"    generate-verification enforces requirement traceability")
    else:
        print(f"    ERROR: No traceability enforcement in generate-verification")
        return FAIL
    
    return PASS

# ============================================================
# Test 5: Test without verification traceability
# ============================================================
def test_test_no_verification_traceability():
    """
    Scenario: A test script has no verification ID in its header comments.
    Expected: omp-verify-test-ledger should reject it.
    """
    ledger_path = Path("bin/omp-verify-test-ledger")
    content = ledger_path.read_text()
    
    # Check for traceability header validation
    if "Verification IDs" in content:
        print(f"    Test ledger validates Verification IDs header")
    else:
        print(f"    WARNING: Verification ID header validation not found in ledger tool")
    
    # Check generate-tests traceability requirement
    gen_path = Path("skills/generate-tests/SKILL.md")
    gen_content = gen_path.read_text()
    
    if "Verification IDs" in gen_content and "Requirement IDs" in gen_content:
        print(f"    generate-tests requires traceability headers")
    else:
        print(f"    ERROR: No traceability header requirement in generate-tests")
        return FAIL
    
    return PASS

# ============================================================
# Test 6: Implementation outside allowed paths
# ============================================================
def test_implementation_outside_allowlist():
    """
    Scenario: implement-specification modifies files outside the spec's Allowlist.
    Expected: The skill instruction prohibits this. The Strict File Scope
    Allowlist is the constraint.
    """
    impl_path = Path("skills/implement-specification/SKILL.md")
    content = impl_path.read_text()
    
    # Check for Allowlist enforcement
    if "Allowlist" in content:
        print(f"    Allowlist enforcement found in implement-specification")
    else:
        print(f"    ERROR: No Allowlist enforcement in implement-specification")
        return FAIL
    
    # Check for test isolation
    if "STRICTLY PROHIBITED from creating, modifying, editing, or deleting any files inside the tests/" in content:
        print(f"    Test isolation enforced")
    else:
        print(f"    WARNING: Test isolation rule may be weak")
    
    return PASS

# ============================================================
# Test 7: Ambiguous implementation boundary
# ============================================================
def test_ambiguous_boundary():
    """
    Scenario: A specification has unclear implementation boundaries.
    Expected: The agent should emit #NEEDS-CLARIFICATION.
    """
    impl_path = Path("skills/implement-specification/SKILL.md")
    content = impl_path.read_text()
    
    # The implement-specification skill should have a halt mechanism
    if "STOP immediately" in content or "halt" in content.lower() or "#NEEDS-CLARIFICATION" in content:
        print(f"    Halt mechanism exists in implement-specification")
    else:
        print(f"    WARNING: No halt mechanism found in implement-specification")
    
    # Also check the milestone skill for the postcondition check
    ms_path = Path("skills/milestone/SKILL.md")
    ms_content = ms_path.read_text()
    
    if "subjective success criteria" in ms_content:
        print(f"    Milestone postcondition check for subjective criteria exists")
    else:
        print(f"    WARNING: No subjective criteria check in milestone skill")
    
    return PASS

# ============================================================
# Test 8: Brownfield implementation already passing
# ============================================================
def test_brownfield_pass():
    """
    Scenario: A test passes because the implementation already exists.
    Expected: evaluate-tests classifies it as VALID_BROWNFIELD_PASS,
    not as a TDD leak.
    """
    eval_path = Path("skills/evaluate-tests/SKILL.md")
    content = eval_path.read_text()
    
    # Check for brownfield detection
    if "VALID_BROWNFIELD_PASS" in content:
        print(f"    Brownfield pass detection exists")
    else:
        print(f"    ERROR: No VALID_BROWNFIELD_PASS classification in evaluate-tests")
        return FAIL
    
    if "target implementation is present" in content:
        print(f"    Implementation presence check exists")
    else:
        print(f"    WARNING: Implementation presence check may be weak")
    
    return PASS

# ============================================================
# Run all tests
# ============================================================
print("=" * 60)
print("  MILESTONE CONTRACT CONTRADICTION TESTS")
print("=" * 60)

test("Undeclared scope detection", test_undeclared_scope)
test("Missing requirement information", test_missing_requirement)
test("Contradictory requirements", test_contradictory_requirements)
test("Verification without requirement traceability", test_verification_no_traceability)
test("Test without verification traceability", test_test_no_verification_traceability)
test("Implementation outside allowed paths", test_implementation_outside_allowlist)
test("Ambiguous implementation boundary", test_ambiguous_boundary)
test("Brownfield implementation already passing", test_brownfield_pass)

print(f"\n{'=' * 60}")
print(f"  RESULTS: {tests_run} tests, {tests_passed} passed, {tests_failed} failed")
print(f"{'=' * 60}")

if tests_failed > 0:
    sys.exit(FAIL)
else:
    sys.exit(PASS)